package io.crate.cratedemo;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class MainActivity extends ActionBarActivity {
    ListView list;
    ArrayList<HashMap<String, String>> stepslist = new ArrayList<HashMap<String, String>>();

    String url = "http://st01p.aws.fir.io:4200/_sql?pretty";

    private static final String TAG_STEPSROW = "rows";
    private static final String TAG_STEPS = "steps";
    private static final String TAG_DATE = "date";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        stepslist = new ArrayList<HashMap<String, String>>();

        RequestQueue queue = Volley.newRequestQueue(this);


        JSONObject params = new JSONObject();
        try {
            params.put("stmt", "SELECT date_trunc('day', ts), sum(num_steps) FROM steps WHERE username = 'gosinski' AND month_partition = '201409' GROUP BY 1 limit 100");
        } catch (JSONException e) {
        }

        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.POST, url, params, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONArray stepentries = response.getJSONArray(TAG_STEPSROW);
                            for (int i = 0; i < stepentries.length(); i++) {
                                JSONArray stepentry = stepentries.getJSONArray(i);
                                String date = stepentry.getString(0);
                                String steps = stepentry.getString(1);
                                HashMap<String, String> map = new HashMap<String, String>();

                                map.put(TAG_DATE, date);
                                map.put(TAG_STEPS, steps);

                                stepslist.add(map);
                                list = (ListView) findViewById(R.id.list);

                                ListAdapter adapter = new SimpleAdapter(MainActivity.this, stepslist,
                                        R.layout.list,
                                        new String[]{TAG_DATE, TAG_STEPS}, new int[]{
                                        R.id.date, R.id.steps});

                                list.setAdapter(adapter);

                            }


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