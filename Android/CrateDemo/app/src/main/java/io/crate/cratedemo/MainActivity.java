package io.crate.cratedemo;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

//        TextView mTxtDisplay;
//        ImageView mImageView;
//
//        mTxtDisplay = (TextView) findViewById(R.id.txtDisplay);
        RequestQueue queue = Volley.newRequestQueue(this);

        String url = "http://st01p.aws.fir.io:4200/_sql?pretty";
        JSONObject params = new JSONObject();
        try {
            params.put("stmt", "SELECT date_trunc('day', ts), sum(num_steps) FROM steps WHERE username = 'gosinski' AND month_partition = '201409' GROUP BY 1 limit 100");
        }
        catch(JSONException e){}

        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.POST, url, params, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        //mTxtDisplay.setText("Response: " + response.toString());
                        Log.v("TAG",response.toString());
                        try {
//                            JSONObject obj = new JSONObject(response);
                            JSONArray m_jArry = response.getJSONArray("rows");
                            String[] rowsArray = new String[m_jArry.length()];
                            Log.v("TAG ",m_jArry.toString());

                            for (int i = 0; i < m_jArry.length(); i++) {
                                TextView greetingIdText = (TextView) findViewById(R.id.id_value);
                                TextView greetingContentText = (TextView) findViewById(R.id.content_value);
                                greetingIdText.setText(greeting.getId());
                                greetingContentText.setText(greeting.getContent());
                            }
//                            Globals g = Globals.getInstance();
//                            g.setData(answersArray);

                        } catch (Exception ex) {
                            Log.e("log_tag", "Error getJSON " + ex.toString());
                        }
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO Auto-generated method stub
                        Log.v("TAG", error.toString());

                    }
                });
        queue.add(jsObjRequest);

// Access the RequestQueue through your singleton class.
        //MySingleton.getInstance(this).addToRequestQueue(jsObjRequest);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}