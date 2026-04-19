'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { MagicPrompt } = require('../src/index');
const { caveman } = require('../src/plugins/caveman');

describe('caveman plugin', () => {
  it('replaces "I" with "me"', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('I want food'), 'Me want food');
  });

  it('removes articles', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('Give me the apple'), 'Give me apple');
  });

  it('replaces "I am" with "me"', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('I am hungry'), 'Me hungry');
  });

  it('replaces "would like to" with "want"', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('I would like to eat'), 'Me want eat');
  });

  it('replaces "create" with "make"', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('Create a website'), 'Make website');
  });

  it('replaces "should" with "must"', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.equal(mp.transform('You should go'), 'You must go');
  });

  it('handles a full prompt', () => {
    const mp = new MagicPrompt().use(caveman);
    const input = 'I would like to generate a solution for the problem.';
    const output = mp.transform(input);
    assert.ok(output.includes('me') || output.includes('Me'), 'should have caveman pronoun');
    assert.ok(!output.includes('I would like to'), 'should replace I would like to');
    assert.ok(!output.includes(' a ') || !output.includes(' the '), 'should remove articles');
  });

  it('throws if plugin has no transform method', () => {
    const mp = new MagicPrompt();
    assert.throws(() => mp.use({}), /transform/);
  });

  it('throws if input is not a string', () => {
    const mp = new MagicPrompt().use(caveman);
    assert.throws(() => mp.transform(42), /string/);
  });

  it('plugins can be chained', () => {
    const upper = { transform: (t) => t.toUpperCase() };
    const mp = new MagicPrompt().use(caveman).use(upper);
    const result = mp.transform('I want food');
    assert.equal(result, 'ME WANT FOOD');
  });
});
