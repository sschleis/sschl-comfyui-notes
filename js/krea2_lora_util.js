import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";

async function fetchLoraList() {
    try {
        const resp = await api.fetchApi("/models/loras");
        if (!resp.ok) return [];
        const data = await resp.json();
        return Array.isArray(data) ? data : [];
    } catch (e) {
        console.error("Krea2LoraUtil: failed to fetch lora list", e);
        return [];
    }
}

app.registerExtension({
    name: "sschl.notes.krea2_lora_util",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "Krea2LoraUtil") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

            this.serialize_widgets = true;
            this._manualLoraCount = 0;
            this._availableLoras = ["None"];

            fetchLoraList().then((loras) => {
                this._availableLoras = ["None", ...loras];
                for (const w of this.widgets) {
                    if (w.name && w.name.startsWith("manual_lora_") && w.name.endsWith("_name")) {
                        w.options = w.options || {};
                        w.options.values = this._availableLoras;
                    }
                }
            });

            this._addLoraButton = this.addWidget("button", "➕ Add Lora", null, () => {
                this.addManualLoraRow();
            });
            this._removeLoraButton = this.addWidget("button", "➖ Remove Last Lora", null, () => {
                this.removeLastManualLoraRow();
            });

            return r;
        };

        nodeType.prototype.addManualLoraRow = function (data) {
            this._manualLoraCount++;
            const index = this._manualLoraCount;
            const loras = this._availableLoras && this._availableLoras.length ? this._availableLoras : ["None"];

            this.addWidget("toggle", `manual_lora_${index}_enabled`, data?.enabled ?? true, () => {});
            this.addWidget("combo", `manual_lora_${index}_name`, data?.name ?? loras[0], () => {}, {
                values: loras,
            });
            this.addWidget("number", `manual_lora_${index}_strength`, data?.strength ?? 1.0, () => {}, {
                min: -2.0,
                max: 2.0,
                step: 0.01,
            });

            // Keep the Add/Remove buttons below the lora rows.
            for (const btn of [this._addLoraButton, this._removeLoraButton]) {
                const idx = this.widgets.indexOf(btn);
                if (idx > -1) {
                    this.widgets.splice(idx, 1);
                    this.widgets.push(btn);
                }
            }

            this.setSize(this.computeSize());
            app.graph.setDirtyCanvas(true, true);
        };

        nodeType.prototype.removeLastManualLoraRow = function () {
            if (this._manualLoraCount <= 0) return;
            const index = this._manualLoraCount;
            this.widgets = this.widgets.filter(
                (w) => !w.name || !w.name.startsWith(`manual_lora_${index}_`)
            );
            this._manualLoraCount--;
            this.setSize(this.computeSize());
            app.graph.setDirtyCanvas(true, true);
        };

        const onConfigure = nodeType.prototype.configure;
        nodeType.prototype.configure = function (info) {
            if (info?.widgets_values) {
                const fixedWidgetCount = 5; // character, lora_strength, realistic, add-button, remove-button
                const remaining = info.widgets_values.length - fixedWidgetCount;
                const rowCount = Math.max(0, Math.floor(remaining / 3));
                while (this._manualLoraCount < rowCount) {
                    this.addManualLoraRow();
                }
            }
            return onConfigure ? onConfigure.apply(this, arguments) : undefined;
        };
    },
});
