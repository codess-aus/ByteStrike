using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

public class LeagueHQ
{
    private static readonly Regex SecretPattern = new Regex(@"\{\* (.*?) \*\}", RegexOptions.Compiled);

    public static string ReadBlueprint(string filename) => File.ReadAllText(filename);

    public static List<string> ExtractSecrets(string content) =>
        SecretPattern.Matches(content)
                     .Select(m => m.Groups[1].Value)
                     .ToList();

    public static Dictionary<string, int> CategorizeSecrets(List<string> secrets) =>
        secrets.GroupBy(s => s.Contains(':') ? s.Split(':')[0].Trim() : "UNKNOWN")
               .ToDictionary(g => g.Key, g => g.Count());

    public static List<string> DecodeBlueprintSafe(string filename)
    {
        try
        {
            return ExtractSecrets(ReadBlueprint(filename));
        }
        catch (FileNotFoundException)
        {
            System.Console.WriteLine($"Error: '{filename}' not found.");
            return new List<string>();
        }
    }
}
