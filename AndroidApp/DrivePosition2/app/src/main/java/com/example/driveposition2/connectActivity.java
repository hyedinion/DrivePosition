package com.example.driveposition2;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.os.Parcelable;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.view.ViewDebug;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.driveposition2.Model.CarModel;

import org.json.JSONException;
import org.json.JSONObject;


import io.socket.client.Socket;
import io.socket.emitter.Emitter;

public class connectActivity extends AppCompatActivity {

    private Socket mSocket;
    DBHelper helper;
    SQLiteDatabase db;
    Integer id = 1242134;
    Integer height = 0;
    EditText edit_height;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.connect);
        edit_height = (EditText)findViewById(R.id.edit_height);


        socketApplication app = (socketApplication) getApplication();
        mSocket = app.getSocket();

        mSocket.on("connect_response", connect_response);

        //db연결
        helper = new DBHelper(connectActivity.this, "newdb.db", null, 1);
        db = helper.getWritableDatabase();
        helper.onCreate(db);


        String sql;
        sql = "select height from mytable where id='" +id+ "';";
        Cursor c = db.rawQuery(sql, null);
        int cnt = c.getCount();
        //height를 입력 안했을 때
        if (cnt!=0){
            while(c.moveToNext()){
                height = c.getInt(0);
            }
            edit_height.setText(height.toString());

        }
    }

    public void onClick(View view){
        mSocket.emit("connect_first","connect");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        mSocket.off("connect_response", connect_response);
    }

    private Emitter.Listener connect_response = new Emitter.Listener() {
        @Override
        public void call(Object... args) {
            String s = args[0].toString();

            String h = edit_height.getText().toString();
            if (h.length()==0){
                connectActivity.this.runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(connectActivity.this, "enter height", Toast.LENGTH_SHORT).show();
                    }
                });
            }
            else{
                Intent intent = new Intent(connectActivity.this, MainActivity.class);
                intent.putExtra("data", s);
                intent.putExtra("height", h);
                startActivity(intent);
            }
        }
    };
}