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

    static void Main()
    {
        var secrets = DecodeBlueprint("blueprint-data.txt");
        Console.WriteLine($"Found {secrets.Count} secret(s):");
        for (int i = 0; i < secrets.Count; i++)
        {
            Console.WriteLine($"{i + 1}. {secrets[i]}");
        }
    }
}
