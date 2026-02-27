using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections.Generic;

public class BlueprintDecoder
{
    public static List<string> DecodeBlueprint(string filename)
    {
        string content = File.ReadAllText(filename);

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
        try
        {
            return DecodeBlueprint(filename);
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"Error: File '{filename}' not found.");
            return new List<string>();
        }
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
