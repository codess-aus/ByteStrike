/**
 * Calculate the area of a triangle given three side lengths using Heron's formula.
 * @param {number} a Length of side A
 * @param {number} b Length of side B
 * @param {number} c Length of side C
 * @returns {number} The area of the triangle
 */
function calculate(a, b, c) {
    const s = (a + b + c) / 2;
    return Math.sqrt(s * (s - a) * (s - b) * (s - c));
}

module.exports = { calculate };
