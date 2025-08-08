
import { app } from "/scripts/app.js";

app.registerExtension({
    name: "sschl.notes.gallery",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Gallery") {
            // Monkey patch the onNodeCreated method to add our custom widget
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                // Create the widget container
                const widgetContainer = document.createElement('div');
                widgetContainer.className = 'sschl-gallery-widget';

                // Add styles directly to the widget
                const style = document.createElement('style');
                style.textContent = `
                    .sschl-gallery-widget {
                        width: 100%;
                        height: 100%; /* Fill the available height */
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(128px, 1fr));
                        gap: 4px;
                        padding: 4px;
                        box-sizing: border-box;
                        overflow-y: auto; /* Add scrollbar if content overflows */
                    }
                    .sschl-gallery-widget img {
                        width: 100%;
                        height: 100%;
                        object-fit: contain; /* Show full image without cropping */
                        cursor: pointer;
                    }
                    .sschl-gallery-overlay {
                        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                        background: rgba(0,0,0,0.85); display: flex;
                        justify-content: center; align-items: center; z-index: 1000;
                    }
                    .sschl-gallery-overlay img { max-width: 90vw; max-height: 90vh; }
                `;
                widgetContainer.appendChild(style);

                // Add the DOM widget to the node
                this.addDOMWidget("gallery", "div", widgetContainer);
                this.galleryContainer = widgetContainer;

                // Add a resize handler to redraw on node resize
                const onResize = this.onResize;
                this.onResize = function() {
                    onResize?.apply(this, arguments);
                    this.setDirtyCanvas(true, true);
                }
            };

            // Monkey patch onExecuted to display the images
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (this.galleryContainer && message?.gallery_images) {
                    // Clear previous images, but keep the style element
                    while (this.galleryContainer.children.length > 1) {
                        this.galleryContainer.removeChild(this.galleryContainer.lastChild);
                    }

                    message.gallery_images.forEach(imgInfo => {
                        const img = new Image();
                        img.src = `/view?filename=${encodeURIComponent(imgInfo.filename)}&type=${imgInfo.type}&subfolder=${encodeURIComponent(imgInfo.subfolder)}`;
                        img.onclick = () => {
                            const overlay = document.createElement('div');
                            overlay.className = 'sschl-gallery-overlay';
                            const fullImg = new Image();
                            fullImg.src = img.src;
                            overlay.appendChild(fullImg);
                            overlay.onclick = () => overlay.remove();
                            document.body.appendChild(overlay);
                        };
                        this.galleryContainer.appendChild(img);
                    });
                }
                this.setDirtyCanvas(true, true);
            };
            
            // Monkey patch onConnectionsChange for dynamic inputs
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                onConnectionsChange?.apply(this, arguments);

                if (!this.inputs) return; // Guard against calls before initialization

                // Add a new input if all existing IMAGE inputs are connected
                const imageInputs = this.inputs.filter(i => i.type === "IMAGE");
                const allConnected = imageInputs.every(i => i.link !== null);
                if (allConnected) {
                    this.addInput(`image_${imageInputs.length}`, "IMAGE");
                }

                // Remove trailing, unconnected image inputs
                for (let i = this.inputs.length - 1; i >= 0; i--) {
                    const input = this.inputs[i];
                    if (input.name.startsWith("image_") && input.link === null) {
                        const nextInput = this.inputs[i+1];
                        if(nextInput && nextInput.name.startsWith("image_")){
                             this.removeInput(i);
                        }
                    } else {
                        break;
                    }
                }
                this.setDirtyCanvas(true, true);
            };
        }
    },
});
