import { app } from "/scripts/app.js";

app.registerExtension({
    name: "sschl.notes.character_prompt_lora",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CharacterPromptWithLora" || nodeData.name === "CharacterPromptWithLoraWithDualModel") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                this.extraLoraCount = 1;
            };

            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function () {
                onConfigure?.apply(this, arguments);
                this.extraLoraCount = 1;
                for (const input of this.inputs || []) {
                    if (input.name.startsWith("extra_lora_")) {
                        const num = parseInt(input.name.split("_").pop());
                        if (num >= this.extraLoraCount) {
                            this.extraLoraCount = num + 1;
                        }
                    }
                }
            };

            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                onConnectionsChange?.apply(this, arguments);
                if (!this.inputs) return;
                this._updateExtraLoraInputs();
            };

            nodeType.prototype._updateExtraLoraInputs = function () {
                const loraInputs = this.inputs.filter(i => i.name.startsWith("extra_lora_"));
                const maxNum = Math.max(0, ...loraInputs.map(i => parseInt(i.name.split("_").pop()) || 0));

                const lastLoraIndex = this.inputs.findIndex(i => i.name === `extra_lora_${maxNum}`);
                const hasNull = loraInputs.some(i => i.link === null && i.name === `extra_lora_${maxNum}`);

                if (hasNull && maxNum > 0) {
                    const nextNum = maxNum;
                    this.addInput(`extra_lora_strength_${nextNum}`, "FLOAT");
                    this.addInput(`extra_lora_${nextNum + 1}`, "COMBO");
                }
            };

            const getExtraMenuOptions = nodeType.prototype.getExtraMenuOptions;
            nodeType.prototype.getExtraMenuOptions = function (_, options) {
                const r = getExtraMenuOptions?.apply(this, arguments);
                options.push({
                    content: "Add LoRA Slot",
                    callback: () => {
                        this.extraLoraCount++;
                        const num = this.extraLoraCount;
                        this.addInput(`extra_lora_${num}`, "COMBO");
                        this.addInput(`extra_lora_strength_${num}`, "FLOAT");
                    }
                });
                if (this.inputs) {
                    const loraInputs = this.inputs.filter(i => i.name.startsWith("extra_lora_"));
                    if (loraInputs.length > 1) {
                        options.push({
                            content: "Remove Last LoRA Slot",
                            callback: () => {
                                const nums = loraInputs.map(i => parseInt(i.name.split("_").pop())).sort((a, b) => b - a);
                                const maxNum = nums[0];
                                if (maxNum > 1) {
                                    for (let i = this.inputs.length - 1; i >= 0; i--) {
                                        const input = this.inputs[i];
                                        if (input.name.endsWith(`_${maxNum}`)) {
                                            this.removeInput(i);
                                        }
                                    }
                                    this.extraLoraCount = maxNum - 1;
                                }
                            }
                        });
                    }
                }
                return r;
            };
        }
    }
});
