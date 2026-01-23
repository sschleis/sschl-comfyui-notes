import { app } from "/scripts/app.js";

app.registerExtension({
    name: "sschl.notes.group_manager",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "GroupManager") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                this.serialize_widgets = true;
                this.isVirtualNode = true;
                return r;
            };

            const onAdded = nodeType.prototype.onAdded;
            nodeType.prototype.onAdded = function() {
                const r = onAdded ? onAdded.apply(this, arguments) : undefined;
                this.updateGroups();
                return r;
            }

            nodeType.prototype.updateGroups = function() {
                if (!app.graph) return;
                
                const groups = app.graph._groups || [];
                const currentWidgets = new Set();

                const setGroupNodesMode = (group, mute) => {
                    const nodesInGroup = group.getNodes();
                    const mode = mute ? 2 : 0; // 2: Never, 0: Always
                    for (const node of nodesInGroup) {
                        node.mode = mode;
                    }
                };

                // Find existing group widgets and sync them
                if (this.widgets) {
                    for (let i = this.widgets.length - 1; i >= 0; i--) {
                        const w = this.widgets[i];
                        if (w.name.startsWith("group_")) {
                            const groupTitle = w.name.substring(6);
                            const group = groups.find(g => g.title === groupTitle);
                            if (group) {
                                currentWidgets.add(groupTitle);
                                // Sync mute state and node modes if it changed
                                const newMute = !w.value;
                                if (group.mute !== newMute) {
                                    group.mute = newMute;
                                    setGroupNodesMode(group, newMute);
                                }
                            } else {
                                // Group no longer exists
                                this.widgets.splice(i, 1);
                            }
                        }
                    }
                }

                // Add missing group widgets
                for (const group of groups) {
                    if (!currentWidgets.has(group.title)) {
                        const widget = this.addWidget("toggle", "group_" + group.title, !group.mute, (v) => {
                            const mute = !v;
                            group.mute = mute;
                            setGroupNodesMode(group, mute);
                            app.graph.setDirtyCanvas(true);
                        });
                        widget.name = "group_" + group.title;
                    }
                }

                this.setSize(this.computeSize());
                app.graph.setDirtyCanvas(true);
            };

            // Periodically check for group changes
            const onExecutionStart = nodeType.prototype.onExecutionStart;
            nodeType.prototype.onExecutionStart = function() {
                onExecutionStart?.apply(this, arguments);
                this.updateGroups();
            };
            
            // Or use a more frequent update if needed
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = function() {
                onDrawForeground?.apply(this, arguments);
                // Simple throttling or just check if count changed
                const groupCount = (app.graph._groups || []).length;
                if (this._lastGroupCount !== groupCount) {
                    this.updateGroups();
                    this._lastGroupCount = groupCount;
                }
            }
        }
    }
});
