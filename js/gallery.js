
import { app } from "/scripts/app.js";

app.registerExtension({
    name: "sschl.notes.gallery",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Gallery") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                this.galleryWidget = this.addDOMWidget("gallery", "div", `
                    <div class="sschl-gallery-widget">
                        <style>
                            .sschl-gallery-widget {
                                width: 100%;
                                height: 100%;
                                display: grid;
                                grid-template-columns: repeat(auto-fill, minmax(128px, 1fr));
                                gap: 5px;
                                padding: 5px;
                                box-sizing: border-box;
                            }
                            .sschl-gallery-widget img {
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                                cursor: pointer;
                            }
                            .sschl-gallery-overlay {
                                position: fixed;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                background: rgba(0,0,0,0.8);
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                z-index: 9999;
                            }
                            .sschl-gallery-overlay img {
                                max-width: 90%;
                                max-height: 90%;
                            }
                        </style>
                    </div>
                `);
                this.galleryWidget.div = this.galleryWidget.element.querySelector('.sschl-gallery-widget');
            };

            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                if (message?.images) {
                    this.galleryWidget.div.innerHTML = ""; // Clear previous images
                    message.images.forEach(imgInfo => {
                        const img = new Image();
                        // The view API needs filename, type and subfolder to find the image
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
                        this.galleryWidget.div.appendChild(img);
                    });
                }
                this.setDirtyCanvas(true, true);
            };
            
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                onConnectionsChange?.apply(this, arguments);

                // Add a new input if the last one is connected
                const lastInput = this.inputs[this.inputs.length - 1];
                if (this.inputs.every(i => i.link !== null)) {
                     this.addInput(`image_${this.inputs.length}`, "IMAGE");
                }

                // Remove unconnected inputs except for the very first one
                for (let i = this.inputs.length - 1; i > 0; i--) {
                    const input = this.inputs[i];
                    if (input.name.startsWith("image_") && input.link === null) {
                        if (i < this.inputs.length -1) {
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
