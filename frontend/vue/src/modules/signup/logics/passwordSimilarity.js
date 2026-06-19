import { computed, toValue } from 'vue'

function longestMatchingBlock(a, b, aStart, aEnd, bStart, bEnd) {
  let bestI = aStart;
  let bestJ = bStart;
  let bestSize = 0;

  for (let i = aStart; i < aEnd; i++) {
    for (let j = bStart; j < bEnd; j++) {
      let k = 0;
      while (i + k < aEnd && j + k < bEnd && a[i + k] === b[j + k]) {
        k++;
      }
      if (k > bestSize) {
        bestI = i;
        bestJ = j;
        bestSize = k;
      }
    }
  }

  return [bestI, bestJ, bestSize];
}

function totalMatchedLength(a, b) {
  let total = 0;
  const stack = [[0, a.length, 0, b.length]];

  while (stack.length) {
    const [aStart, aEnd, bStart, bEnd] = stack.pop();
    const [i, j, k] = longestMatchingBlock(a, b, aStart, aEnd, bStart, bEnd);

    if (k === 0) continue;

    total += k;

    if (aStart < i && bStart < j) {
      stack.push([aStart, i, bStart, j]);
    }
    if (i + k < aEnd && j + k < bEnd) {
      stack.push([i + k, aEnd, j + k, bEnd]);
    }
  }

  return total;
}

export function similarityRatio(a, b) {
  if (!a || !b) return 0;
  const matched = totalMatchedLength(a, b);
  return (2 * matched) / (a.length + b.length);
}

export function validatePasswordSimilarity(password, user, options = {}) {
  const { maxSimilarity = 0.7 } = options;

  if (!password || !user || typeof user !== 'string') {
    return true;
  }
  const ratio = similarityRatio(password.toLowerCase(), user.toLowerCase());

  return ratio < maxSimilarity;
}

export function usePasswordSimilarityValidator(password, user, options = {}) {
  const validation = computed(() =>
    validatePasswordSimilarity(toValue(password), toValue(user), options)
  )
  return validation;
}
