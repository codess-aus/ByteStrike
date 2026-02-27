/**
 * @param {{ name: string }[]} data
 * @returns {string[]}
 */
function extractNames(data) {
    // Extract the 'name' field from each object and return as a list of strings
    return data.map((item) => item.name);
}

module.exports = { extractNames };
