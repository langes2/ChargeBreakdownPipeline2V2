using System;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;

class Apitester
{
    static async Task Main(string[] args)
    {
        // Fetch the API token using TokenFetcher
        TokenFetcher tokenFetcher = new TokenFetcher();
        string apiToken = await tokenFetcher.GetApiToken();

        if (string.IsNullOrEmpty(apiToken))
        {
            Console.WriteLine("Failed to retrieve API token.");
            return;
        }

        // Initialize HttpClient
        using (HttpClient client = new HttpClient())
        {
            client.Timeout = TimeSpan.FromMinutes(15);
            client.BaseAddress = new Uri("https://della.api.rentmanager.com/");

            // Set up the request headers
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            client.DefaultRequestHeaders.Add("X-RM12Api-ApiToken", apiToken);
            client.DefaultRequestHeaders.Add("X-RM12Api-locationID", "4");

            // Get first of month date and current date
            /*
            DateTime firstDayOfCurrentMonth = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1);
            DateTime currentDate = DateTime.Now;

            string startDate = firstDayOfCurrentMonth.ToString("MM/dd/yy");
            string endDate = currentDate.ToString("MM/dd/yy");
            */

            DateTime firstDayOfPreviousMonth = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1).AddMonths(-1);
            DateTime lastDayOfPreviousMonth = new DateTime(DateTime.Now.Year, DateTime.Now.Month, 1).AddDays(-1);

            string startDate = firstDayOfPreviousMonth.ToString("MM/dd/yy");
            string endDate = lastDayOfPreviousMonth.ToString("MM/dd/yy");

            HttpResponseMessage response = await client.GetAsync($"/Reports/29/RunReport?parameters=ChargeTypeOrder,(2,3,4,7,8,10,15,16,17,38,39,54);StartDate,{startDate};EndDate,{endDate}&GetOptions=ReturnExcelStream");
            try
            {
                response.EnsureSuccessStatusCode();
            }
            catch (HttpRequestException ex)
            {
                if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return;
                }
                else
                {
                    throw ex;
                }
            }

            // Generate the folder and file path with the current date
            string useDate = lastDayOfPreviousMonth.ToString("MM_dd_yy");

            // Base folder path
            string baseReportPath = @"C:\Users\Public\Documents\CBfrags";
            
            // Create a new subfolder with the current date
            string datedFolderPath = Path.Combine(baseReportPath, $"CBfragsmonthly{useDate}");
            Directory.CreateDirectory(datedFolderPath); // Ensure the dated folder exists

            // Create the file path inside the new folder
            string reportFile = Path.Combine(datedFolderPath, $"ChargeBreakdown{useDate}frag1.xlsx");

            // Handle the report stream
            Stream reportStream = response.Content.ReadAsStreamAsync().Result;
            if (reportStream.GetType().Name == "MemoryStream")
            {
                if (File.Exists(reportFile))
                {
                    File.Delete(reportFile);
                }

                using (Stream fileStream = File.Create(reportFile))
                {
                    reportStream.CopyTo(fileStream);
                }

                reportStream.Close();
            }
        }
    }
}
