using System;
using System.Collections.Generic;

public static class UrlValidator
{
    private static readonly HashSet<string> AllowedHosts = new()
    {
        "raw.githubusercontent.com",
        "league-blueprints.internal"
    };

    /// <summary>Throw ArgumentException if URL is not HTTPS or host is not allowed.</summary>
    public static void ValidateUrl(string url)
    {
        var uri = new Uri(url);
        if (uri.Scheme != "https")
            throw new ArgumentException($"URL must use HTTPS. Got: '{uri.Scheme}'");
        if (!AllowedHosts.Contains(uri.Host))
            throw new ArgumentException($"Host '{uri.Host}' is not in the allowed list.");
    }
}
