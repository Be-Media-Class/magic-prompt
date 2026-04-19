'use strict';

class MagicPrompt {
  constructor() {
    this.plugins = [];
  }

  use(plugin) {
    if (typeof plugin.transform !== 'function') {
      throw new Error(`Plugin must implement a transform(text) method`);
    }
    this.plugins.push(plugin);
    return this;
  }

  transform(text) {
    if (typeof text !== 'string') throw new TypeError('Input must be a string');
    return this.plugins.reduce((acc, plugin) => plugin.transform(acc), text);
  }
}

module.exports = { MagicPrompt };
