const fs = require("fs");

/**
 * Reads a blueprint file and extracts all secrets marked between {* and *}
 * Example: League transmission contains {* EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE *}
 * Extracts: "EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE" (without markers)
 * Uses regex pattern with match() or matchAll()
 * @param {string} filename - Path to the blueprint file
 * @returns {Array<string>} Array of extracted secret strings
 */
function decodeBlueprint(filename) {
    const content = fs.readFileSync(filename, "utf8");

    // Use regex to find all secrets between {* and *}
    const pattern = /\{\* (.*?) \*\}/g;
    const matches = [...content.matchAll(pattern)];
    const secrets = matches.map((match) => match[1]);

    return secrets;
}

// Test the decoder
const secrets = decodeBlueprint("blueprint-data.txt");
console.log(`Found ${secrets.length} secret(s):`);
secrets.forEach((secret, index) => {
    console.log(`${index + 1}. ${secret}`);
});

module.exports = { decodeBlueprint };
