import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Created by Matt on 12/10/2014.
 */
public class GetAccountBalance extends HttpServlet
{
  protected void doGet(HttpServletRequest request,
                       HttpServletResponse response)
          throws ServletException, IOException
  {
    String custId = request.getParameter("custId");

    DataAccess dataAccess = new DataAccess();
    try
    {
      dataAccess.open();
      double accountBalance = dataAccess.getAccountBalance(custId);
      JSONObject balObj = new JSONObject();
      balObj.put("accountbalance", accountBalance);
      response.getWriter().print(balObj.toString());
    } catch (SQLException e)
    {
      e.printStackTrace();
    } catch (JSONException e)
    {
      e.printStackTrace();
    }
  }
}
