using NUnit.Framework;
using System.Collections.Generic;

[TestFixture]
public class BlueprintDecoderTests
{
    [Test]
    public void ExtractSecrets_FindsAllSecrets()
    {
        var content = "data {* SECRET_ONE *} more {* KEY: VALUE *} end";
        var result = BlueprintDecoder.ExtractSecrets(content);
        Assert.That(result, Is.EqualTo(new List<string> { "SECRET_ONE", "KEY: VALUE" }));
    }

    [Test]
    public void ExtractSecrets_NoMatches_ReturnsEmpty()
    {
        Assert.That(BlueprintDecoder.ExtractSecrets("no secrets here"), Is.Empty);
    }

    [Test]
    public void CategorizeSecrets_GroupsByPrefix()
    {
        var secrets = new List<string> { "AGENT_CODENAME: SHADOWMIND", "VAULT_ACCESS_CODE: DELTA-7", "AGENT_CODENAME: GHOSTFIRE" };
        var result = BlueprintDecoder.CategorizeSecrets(secrets);
        Assert.That(result["AGENT_CODENAME"], Is.EqualTo(2));
        Assert.That(result["VAULT_ACCESS_CODE"], Is.EqualTo(1));
    }

    [Test]
    public void CategorizeSecrets_NoColon_MarkedUnknown()
    {
        var result = BlueprintDecoder.CategorizeSecrets(new List<string> { "SECURE_COMMS_PROTOCOL" });
        Assert.That(result["UNKNOWN"], Is.EqualTo(1));
    }
}
