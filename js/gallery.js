
import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";

app.registerExtension({
    name: "sschl.notes.gallery",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Gallery") {
            // Setup the node
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const widgetContainer = document.createElement('div');
                widgetContainer.className = 'sschl-gallery-widget';
                const style = document.createElement('style');
                style.textContent = `
                    .sschl-gallery-widget { width: 100%; height: 100%; display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); grid-auto-rows: minmax(100px, auto); gap: 4px; padding: 4px; box-sizing: border-box; overflow-y: auto; }
                    .sschl-gallery-widget img { width: 100%; height: 100%; object-fit: contain; cursor: pointer; }
                    .sschl-gallery-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; z-index: 1000; }
                    .sschl-gallery-overlay img { max-width: 90vw; max-height: 90vh; }
                `;
                widgetContainer.appendChild(style);
                this.addDOMWidget("gallery", "div", widgetContainer);
                this.galleryContainer = widgetContainer;
            };

            // Handle dynamic inputs
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                onConnectionsChange?.apply(this, arguments);
                if (!this.inputs) return;
                const imageInputs = this.inputs.filter(i => i.type === "IMAGE");
                if (imageInputs.every(i => i.link !== null)) {
                    this.addInput(`image_${imageInputs.length}`, "IMAGE");
                }
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
            };
        }
    },
    init() {
        // Listen for clear messages
        api.addEventListener("sschl-gallery-clear", ({ detail }) => {
            const node = app.graph.getNodeById(detail.node_id);
            if (node && node.galleryContainer) {
                while (node.galleryContainer.children.length > 1) {
                    node.galleryContainer.removeChild(node.galleryContainer.lastChild);
                }
            }
        });

        // Listen for update messages
        api.addEventListener("sschl-gallery-update", ({ detail }) => {
            const node = app.graph.getNodeById(detail.node_id);
            if (node && node.galleryContainer) {
                const imgInfo = detail.image;
                const img = new Image();
                img.src = api.apiURL(`/view?filename=${encodeURIComponent(imgInfo.filename)}&type=${imgInfo.type}&subfolder=${encodeURIComponent(imgInfo.subfolder)}`);
                img.onclick = () => {
                    const overlay = document.createElement('div');
                    overlay.className = 'sschl-gallery-overlay';
                    const fullImg = new Image();
                    fullImg.src = img.src;
                    overlay.appendChild(fullImg);
                    overlay.onclick = () => overlay.remove();
                    document.body.appendChild(overlay);
                };
                node.galleryContainer.appendChild(img);
            }
        });
    }
});
