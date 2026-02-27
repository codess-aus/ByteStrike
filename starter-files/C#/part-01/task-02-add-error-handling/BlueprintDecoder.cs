using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class BlueprintDecoder
{
    /// <summary>
    /// Reads a blueprint file and extracts all secrets marked between {* and *}
    /// Example: {* VAULT_ACCESS_CODE: DELTA-7-7-ECHO *} extracts the code inside
    /// Uses regex pattern to find all occurrences
    /// </summary>
    /// <param name="filename">Path to the blueprint file</param>
    /// <returns>List of extracted secret strings</returns>
    public static List<string> DecodeBlueprint(string filename)
    {
        string content = File.ReadAllText(filename);

        // Use regex to find all secrets between {* and *}
        string pattern = @"\{\* (.*?) \*\}";
        MatchCollection matches = Regex.Matches(content, pattern);

        List<string> secrets = new List<string>();
        foreach (Match match in matches)
        {
            secrets.Add(match.Groups[1].Value);
        }

        return secrets;
    }

    // Enhanced version with error handling
    // If file doesn't exist, return empty list and print error message
    public static List<string> DecodeBlueprintSafe(string filename)
    {
        // TODO: Add try-catch to handle FileNotFoundException
        // TODO: If file doesn't exist, print error message and return empty list
        // TODO: Otherwise, call DecodeBlueprint and return secrets
        return new List<string>();
    }

    static void Main()
    {
        // Test error handling
        var secrets1 = DecodeBlueprintSafe("nonexistent.txt");
        Console.WriteLine($"Found {secrets1.Count} secrets");

        // Test normal operation
        var secrets2 = DecodeBlueprintSafe("blueprint-data.txt");
        Console.WriteLine($"Found {secrets2.Count} secrets");
    }
}
