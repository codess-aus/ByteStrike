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

    // Function to format and display secrets in a professional report
    // Includes header, separator lines, numbered list, and footer
    public static void DisplaySecretsReport(List<string> secrets)
    {
        string separator = new string('=', 50);
        Console.WriteLine("\n" + separator);
        Console.WriteLine("DECODED SECRETS REPORT".PadRight(50));
        Console.WriteLine(separator);
        Console.WriteLine($"Total secrets found: {secrets.Count}\n");
        for (int i = 0; i < secrets.Count; i++)
        {
            Console.WriteLine($"  [{i + 1,2}] {secrets[i]}");
        }
        Console.WriteLine("\n" + separator + "\n");
    }

    // Function to categorize secrets by their type (word before the colon)
    public static Dictionary<string, int> CategorizeSecrets(List<string> secrets)
    {
        var categories = new Dictionary<string, int>();
        foreach (var secret in secrets)
        {
            string category;
            if (secret.Contains(':'))
            {
                category = secret.Split(':')[0].Trim();
            }
            else
            {
                category = "UNCLASSIFIED";
            }

            if (!categories.ContainsKey(category))
            {
                categories[category] = 0;
            }
            categories[category]++;
        }

        return categories;
    }

    static void Main()
    {
        var secrets = DecodeBlueprintSafe("blueprint-data.txt");
        DisplaySecretsReport(secrets);

        var categories = CategorizeSecrets(secrets);
        Console.WriteLine("\nSecret Categories:");
        foreach (var entry in categories)
        {
            Console.WriteLine($"  {entry.Key}: {entry.Value}");
        }
    }
}
