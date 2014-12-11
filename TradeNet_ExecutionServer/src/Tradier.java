import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
import org.json.JSONObject;

/**
 * Created by Matt on 12/9/2014.
 */
public class Tradier
{
  public static double getStockQuote(String stocks) throws IOException
  {
    BufferedReader responseBody = null;
    HttpClient client = HttpClientBuilder.create().build();
    String result = "";
    double sharePrice = 0;
    try
    {
      //Define a HttpGet request
      HttpGet request = new HttpGet("https://sandbox.tradier"
                                    + ".com/v1/markets/quotes?symbols=" + stocks);

      //Set Http Headers
      request.addHeader("Accept", "application/json");
      request.addHeader("Authorization", "Bearer TSCALKvrKOHFY1VH05ML7oMBbil4");

      //Invoke the service
      HttpResponse response = client.execute(request);

      //Verify if the response is valid
      int statusCode = response.getStatusLine().getStatusCode();
      if (statusCode != 200)
      {
        throw new RuntimeException("Failed with HTTP error code : " + statusCode);
      }
      else
      {
        //If valid, get the response
        responseBody = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line = "";
        StringBuilder sb = new StringBuilder(result);
        while ((line = responseBody.readLine()) != null)
        {
          sb.append(line);
        }
        result = sb.toString();
        JSONObject obj = new JSONObject(result);

        sharePrice = Double.parseDouble(
                obj.getJSONObject("quotes").getJSONObject("quote").getString("close"));
      }

    } catch (Exception e)
    {
      BuyStock.status = "OOPS! Something went wrong! Error 20";
    } finally
    {
      if (responseBody != null)
        responseBody.close();
    }
    return sharePrice;
  }
}
