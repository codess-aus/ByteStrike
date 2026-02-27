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

// Function to format and display secrets in a professional report
// Includes header, separator lines, numbered list, and footer
function displaySecretsReport(secrets) {
    const separator = "=".repeat(50);
    console.log("\n" + separator);
    console.log("DECODED SECRETS REPORT".padEnd(50));
    console.log(separator);
    console.log(`Total secrets found: ${secrets.length}\n`);
    secrets.forEach((secret, index) => {
        const num = String(index + 1).padStart(2, " ");
        console.log(`  [${num}] ${secret}`);
    });
    console.log("\n" + separator + "\n");
}

// Function to categorize secrets by their type (word before the colon)
function categorizeSecrets(secrets) {
    const categories = {};
    for (const secret of secrets) {
        const category = secret.includes(":") ? secret.split(":")[0].trim() : "UNCLASSIFIED";
        categories[category] = (categories[category] ?? 0) + 1;
    }
    return categories;
}

// Use it
const secrets = decodeBlueprintSafe("blueprint-data.txt");
displaySecretsReport(secrets);

const categories = categorizeSecrets(secrets);
console.log("\nSecret Categories:");
Object.keys(categories)
    .sort()
    .forEach((category) => {
        console.log(`  ${category}: ${categories[category]}`);
    });

module.exports = {
    decodeBlueprint,
    decodeBlueprintSafe,
    displaySecretsReport,
    categorizeSecrets,
};
