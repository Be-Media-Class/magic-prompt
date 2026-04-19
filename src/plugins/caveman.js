'use strict';

const REPLACEMENTS = [
  // Pronouns — most specific first
  [/\bI would like to\b/gi, 'me want'],
  [/\bI would like\b/gi, 'me want'],
  [/\bI am\b/gi, 'me'],
  [/\bI will\b/gi, 'me will'],
  [/\bI would\b/gi, 'me want'],
  [/\bI'd\b/gi, 'me want'],
  [/\bI'll\b/gi, 'me will'],
  [/\bI've\b/gi, 'me have'],
  [/\bI'm\b/gi, 'me'],
  [/\bI\b/g, 'me'],

  // Articles
  [/\b(a|an|the)\b\s*/gi, ''],

  // Common verbs → caveman
  [/\bwould like to\b/gi, 'want'],
  [/\bwould like\b/gi, 'want'],
  [/\bneed to\b/gi, 'need'],
  [/\bwant to\b/gi, 'want'],
  [/\bwould\b/gi, 'want'],
  [/\bcould\b/gi, 'can'],
  [/\bshould\b/gi, 'must'],
  [/\bhave to\b/gi, 'must'],
  [/\bhas to\b/gi, 'must'],
  [/\bplease\b/gi, ''],
  [/\bcreate\b/gi, 'make'],
  [/\bgenerate\b/gi, 'make'],
  [/\bprovide\b/gi, 'give'],
  [/\bexplain\b/gi, 'tell'],
  [/\bdescribe\b/gi, 'tell about'],
  [/\bwrite\b/gi, 'make'],
  [/\bbuild\b/gi, 'make'],
  [/\banalyze\b/gi, 'look at'],
  [/\banalyse\b/gi, 'look at'],
  [/\butilize\b/gi, 'use'],
  [/\bimprove\b/gi, 'make better'],
  [/\boptimize\b/gi, 'make better'],
  [/\bimplement\b/gi, 'make'],
  [/\bconsider\b/gi, 'think about'],
  [/\battempt\b/gi, 'try'],
  [/\bassist\b/gi, 'help'],
  [/\bhelp me\b/gi, 'help'],

  // Common nouns → caveman
  [/\binformation\b/gi, 'thing'],
  [/\bsolution\b/gi, 'answer'],
  [/\bsolutions\b/gi, 'answers'],
  [/\bquestion\b/gi, 'ask'],
  [/\bquestions\b/gi, 'ask'],
  [/\bexample\b/gi, 'show'],
  [/\bexamples\b/gi, 'show'],
  [/\bapplication\b/gi, 'app'],
  [/\bapplications\b/gi, 'apps'],
  [/\bfunction\b/gi, 'thing do'],
  [/\bfunctions\b/gi, 'things do'],
  [/\bvery\b/gi, 'much'],
  [/\bextremely\b/gi, 'much much'],
  [/\bhowever\b/gi, 'but'],
  [/\btherefore\b/gi, 'so'],
  [/\badditionally\b/gi, 'also'],
  [/\bfurthermore\b/gi, 'and also'],

  // Clean up extra spaces
  [/[ \t]{2,}/g, ' '],
  [/^\s+|\s+$/gm, ''],
];

const caveman = {
  name: 'caveman',

  transform(text) {
    let result = REPLACEMENTS.reduce((acc, [pattern, replacement]) => {
      return acc.replace(pattern, replacement);
    }, text);

    // Capitalise first letter of each sentence
    result = result.replace(/(^\s*|[.!?]\s+)([a-z])/g, (_, before, letter) => {
      return before + letter.toUpperCase();
    });

    return result.trim();
  },
};

module.exports = { caveman };
