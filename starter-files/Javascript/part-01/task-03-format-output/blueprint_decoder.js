const fs = require("fs");

function decodeBlueprint(filename) {
    const content = fs.readFileSync(filename, "utf8");
    const pattern = /\{\* (.*?) \*\}/g;
    const matches = [...content.matchAll(pattern)];
    const secrets = matches.map((match) => match[1]);
    return secrets;
}

// Enhanced version with error handling
// If file doesn't exist, return empty array and print error message
function decodeBlueprintSafe(filename) {
    try {
        return decodeBlueprint(filename);
    } catch (err) {
        console.log(`Error: File '${filename}' not found.`);
        return [];
    }
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
