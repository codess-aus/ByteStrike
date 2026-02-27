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
}
