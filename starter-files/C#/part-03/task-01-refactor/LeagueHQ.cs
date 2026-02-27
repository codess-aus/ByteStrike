using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

public class LeagueHQ
{
    public static Dictionary<string, int> DecodeBlueprint(string filename)
    {
        try
        {
            var content = File.ReadAllText(filename);
            var pattern = new Regex(@"\{\* (.*?) \*\}");
            var secrets = pattern.Matches(content).Select(m => m.Groups[1].Value).ToList();
            Console.WriteLine(new string('=', 40));
            Console.WriteLine("DECODED SECRETS REPORT");
            Console.WriteLine(new string('=', 40));
            Console.WriteLine($"Found {secrets.Count} secret(s):\n");
            for (int i = 0; i < secrets.Count; i++)
                Console.WriteLine($"{i + 1}. {secrets[i]}");
            Console.WriteLine(new string('=', 40));
            var cats = new Dictionary<string, int>();
            foreach (var s in secrets)
            {
                var key = s.Contains(':') ? s.Split(':')[0].Trim() : "UNKNOWN";
                cats[key] = cats.GetValueOrDefault(key, 0) + 1;
            }
            return cats;
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"Error: '{filename}' not found.");
            return new Dictionary<string, int>();
        }
    }
}
