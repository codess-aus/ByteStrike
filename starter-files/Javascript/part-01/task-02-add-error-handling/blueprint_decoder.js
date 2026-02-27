const fs = require("fs");

/**
 * Reads a blueprint file and extracts all secrets marked between {* and *}
 * Example: League transmission contains {* EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE *}
 * Extracts: "EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE" (without markers)
 * Uses regex pattern with matchAll()
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

// Enhanced version with error handling
// If file doesn't exist, return empty array and print error message
function decodeBlueprintSafe(filename) {
    // TODO: Add try-catch to handle file errors
    // TODO: If file doesn't exist, print error and return empty array
    // TODO: Otherwise, call decodeBlueprint and return secrets
    return [];
}

// Test error handling
const secrets1 = decodeBlueprintSafe("nonexistent.txt");
console.log(`Found ${secrets1.length} secrets`);

// Test normal operation
const secrets2 = decodeBlueprintSafe("blueprint-data.txt");
console.log(`Found ${secrets2.length} secrets`);

module.exports = {
    decodeBlueprint,
    decodeBlueprintSafe,
};
