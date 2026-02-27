function process(d) {
    // return the result
    return d;
}

/**
 * @param {{ name: string }[]} items
 * @returns {string[]}
 */
function extractItemNames(items) {
    // iterate over items and return a list of each item's name
    return items.map((item) => item.name);
}

module.exports = { process, extractItemNames };
