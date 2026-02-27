using System.Collections.Generic;
using System.Linq;

public class NamingExperiment
{
    public List<string> Process(List<object> d)
    {
        // return the result
        return d.Select(x => x.ToString()).ToList();
    }

    public List<string> ExtractProductNames(List<Product> products)
    {
        // iterate over products and return a list of each product's name
        return products.Select(p => p.Name).ToList();
    }
}

public class Product
{
    public string Name { get; set; } = string.Empty;
}
