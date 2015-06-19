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
import com.android.volley.toolbox.StringRequest;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;

public class MainActivity extends ActionBarActivity {
    ListView list;
    ArrayList<HashMap<String, String>> eventslist = new ArrayList<HashMap<String, String>>();

    String url = "http://192.168.59.103:8080/events/";

    //private static final String TAG_EVENTSROW = "rows";
    private static final String TAG_CA = "created_at";
    private static final String TAG_TYPE = "type";
    //private static final String TAG_UN = "actor['login']";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        refreshJSON();

    }

    private void refreshJSON() {
        eventslist = new ArrayList<HashMap<String, String>>();

        RequestQueue queue = CustomRequest.getInstance(this).getRequestQueue();

        String type = "PushEvent";
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url + type,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {

                            JSONArray evententries = new JSONArray(response);
                            for (int i = 0; i < evententries.length(); i++) {
                                JSONObject evententry = evententries.getJSONObject(i);

                                //String eventid = evententry.getString("id");
                                String created_at = evententry.getString("created_at");
                                String type = evententry.getString("type");
                                //String un = evententry.getString("actor[\"login\"]");

                                HashMap<String, String> map = new HashMap<String, String>();
                                //map.put(TAG_ID, id);
                                map.put(TAG_TYPE, type);
                                map.put(TAG_CA, created_at);

                                eventslist.add(map);
                                list = (ListView) findViewById(R.id.list);

                                ListAdapter adapter = new SimpleAdapter(MainActivity.this, eventslist,
                                        R.layout.list,

                                        new String[]{TAG_CA, TAG_TYPE}, new int[]{
                                        R.id.created_at, R.id.type});

                                list.setAdapter(adapter);
                            }
                        } catch (Exception ex) {
                            Log.e("log_tag", "Error getJSON " + ex.toString());
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.v("Waiting ", error.toString());
            }
        });
        queue.add(stringRequest);
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