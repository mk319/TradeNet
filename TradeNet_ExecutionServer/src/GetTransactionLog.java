import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Created by Matt on 12/10/2014.
 */
public class GetTransactionLog extends HttpServlet
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
      JSONArray jsonArray = dataAccess.getTransactions(custId);
      response.getWriter().print(jsonArray.toString());
    } catch (SQLException e)
    {
      e.printStackTrace();
    } catch (JSONException e)
    {
      e.printStackTrace();
    }
    finally
    {
      try
      {
        dataAccess.close();
      } catch (SQLException e)
      {
        e.printStackTrace();
      }
    }
  }
}
