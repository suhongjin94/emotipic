package com.example.android.camera2basic;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.facebook.FacebookSdk;
import com.facebook.appevents.AppEventsLogger;
import com.facebook.messenger.MessengerUtils;
import com.facebook.messenger.MessengerThreadParams;
import com.facebook.messenger.ShareToMessengerParams;
import com.koushikdutta.async.future.Future;
import com.koushikdutta.async.future.FutureCallback;
import com.koushikdutta.ion.Ion;
import com.koushikdutta.ion.Response;
import com.microsoft.projectoxford.face.FaceServiceClient;

import com.microsoft.projectoxford.face.*;

import com.microsoft.projectoxford.face.contract.*;
import com.twitter.sdk.android.Twitter;
import com.twitter.sdk.android.core.TwitterAuthConfig;
import com.twitter.sdk.android.core.TwitterCore;
import com.twitter.sdk.android.tweetcomposer.TweetComposer;


import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;

import io.fabric.sdk.android.Fabric;

/**
 * Created by suhon_000 on 11/14/2015.
 */
public class ResultActivity extends Activity implements View.OnClickListener {

    private FaceServiceClient faceServiceClient =
            new FaceServiceClient("6c15189c7c5c4dc3bd57e7bc43b5c5d9");

    private ImageView img;
    private Bitmap origBmp;

    private String path;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Initialize Facebook SDK
        FacebookSdk.sdkInitialize(getApplicationContext());

        // Get Twitter Kit
        TwitterAuthConfig authConfig =  new TwitterAuthConfig("bbIvH1VEjlERSanfcw8ufSGTc", " PZpMe3gybLggHkopxGA5u1HKOOmgYBqeS7IIFpV85i3SAyZuAz");
        Fabric.with(this, new Twitter(authConfig));

        setContentView(R.layout.activity_result);
        path = getIntent().getStringExtra("TESTING");
        origBmp = BitmapFactory.decodeFile(path);
//        try {
//            ExifInterface ei = new ExifInterface(path);
//            int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
//
//            switch(orientation) {
//                case ExifInterface.ORIENTATION_ROTATE_90:
//                    bitmap = rotateImage(bitmap, 90);
//                    break;
//                case ExifInterface.ORIENTATION_ROTATE_180:
////                    bitmap = rotateImage(bitmap, 180);
//                    break;
//                // etc.
//            }
//        } catch (IOException e) {
//
//        }

        img = (ImageView) findViewById(R.id.result_image);
        img.setImageBitmap(origBmp);

        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        origBmp.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream.toByteArray();
        Log.v("TAG", "bytes: " + Integer.toString(byteArray.length));
        String encoded = Base64.encodeToString(byteArray, Base64.NO_WRAP);
        Log.d("TAG", Integer.toString(encoded.length()));
        String url = "http://emotipic.azurewebsites.net/upload";

        byte[] decodedString = Base64.decode(encoded, Base64.DEFAULT);
        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        img.setImageBitmap(decodedByte);
//        new DownloadTask().execute(url, path);
//        detectAndFrame(origBmp);

        Button messengerButton = (Button) findViewById(R.id.messenger_send_button);
        messengerButton.setOnClickListener(this);

        Button twitterButton = (Button) findViewById(R.id.twitter_share);
        twitterButton.setOnClickListener(this);

        File f = new File(path);
        Future uploading = Ion.with(this)
                .load("http://emotipic.azurewebsites.net/upload")
                .setMultipartFile("image", f)
                .asString()
                .withResponse()
                .setCallback(new FutureCallback<Response<String>>() {
                    @Override
                    public void onCompleted(Exception e, Response<String> result) {
                        try {
                            JSONObject jobj = new JSONObject(result.getResult());
                            Toast.makeText(getApplicationContext(), jobj.getString("response"), Toast.LENGTH_SHORT).show();

                        } catch (JSONException e1) {
                            Log.e("TAG", e1.toString());
                        }

                    }
                });

    }

    private void detectAndFrame(final Bitmap imageBitmap) {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        imageBitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream);
        ByteArrayInputStream inputStream = new ByteArrayInputStream(outputStream.toByteArray());
        AsyncTask<InputStream, String, Face[]> detectTask =
                new AsyncTask<InputStream, String, Face[]>() {
                    @Override
                    protected Face[] doInBackground(InputStream... params) {
                        try {
                            publishProgress("Detecting...");
                            Face[] result = faceServiceClient.detect(
                                    params[0], false, false, false, false);
                            if (result == null) {
                                publishProgress("Detection Finished. Nothing detected");
                                Log.v("TAG", "Detection Finished. Nothing detected");
                                return null;
                            }
                            publishProgress(
                                    String.format("Detection Finished. %d face(s) detected",
                                            result.length));
                            return result;
                        } catch (Exception e) {
                            publishProgress("Detection failed");
                            Log.v("TAG", e.toString());
                            return null;
                        }
                    }

                    @Override
                    protected void onPreExecute() {
                        Log.v("TAG", "Starting async");
                    }

                    @Override
                    protected void onProgressUpdate(String... progress) {
                    }

                    @Override
                    protected void onPostExecute(Face[] result) {
                        if (result == null) {
                            Log.v("TAG", "ITS FREAKING NULL");
                            return;
                        }
                        img.setImageBitmap(drawFaceRectanglesOnBitmap(origBmp, result));
                    }

                };

        detectTask.execute(inputStream);

    }

    private static Bitmap drawFaceRectanglesOnBitmap(Bitmap originalBitmap, Face[] faces) {
        Bitmap bitmap = originalBitmap.copy(Bitmap.Config.ARGB_8888, true);
        Canvas canvas = new Canvas(bitmap);
        Paint paint = new Paint();
        paint.setAntiAlias(true);
        paint.setStyle(Paint.Style.STROKE);
        paint.setColor(Color.RED);
        int stokeWidth = 2;
        paint.setStrokeWidth(stokeWidth);
        if (faces != null) {
            for (Face face : faces) {
                FaceRectangle faceRectangle = face.faceRectangle;
                canvas.drawRect(
                        faceRectangle.left,
                        faceRectangle.top,
                        faceRectangle.left + faceRectangle.width,
                        faceRectangle.top + faceRectangle.height,
                        paint);
            }
        }
        return bitmap;
    }

    @Override
    protected void onResume() {
        super.onResume();

        // Logs 'install' and 'app activate' App Events.
        AppEventsLogger.activateApp(this);
    }

    @Override
    protected void onPause() {
        super.onPause();

        // Logs 'app deactivate' App Event.
        AppEventsLogger.deactivateApp(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.messenger_send_button: {
                String mimeType = "image/jpeg";

                // contentUri points to the content being shared to Messenger
                Uri contentUri = Uri.fromFile(new File(path));
                ShareToMessengerParams shareToMessengerParams =
                        ShareToMessengerParams.newBuilder(contentUri, mimeType)
                                .build();

// Sharing from an Activity
                MessengerUtils.shareToMessenger(
                        this,
                        0,
                        shareToMessengerParams);
                break;
            }
            case R.id.twitter_share: {
                Uri contentUri = Uri.fromFile(new File(path));
                TweetComposer.Builder builder = new TweetComposer.Builder(this)
                        .text("just setting up my Fabric.")
                        .image(contentUri);
                builder.show();
            }
        }
    }

    private class DownloadTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {
            try {
                return loadFromNetwork(urls[0], urls[1]);
            } catch (IOException e) {
                return e.toString();
            }
        }

        @Override
        protected void onPreExecute() {
            Log.v("TAG", "Starting POST async");
        }

        @Override
        protected void onPostExecute(String result) {
            Log.i("TAG", "DID POST: " + result);
        }
    }

    /** Initiates the fetch operation. */
    private String loadFromNetwork(String urlString, String image) throws IOException {
        InputStream stream = null;
        String str ="";

        try {
            stream = downloadUrl(urlString, image);
            str = readIt(stream, 500);
        } finally {
            if (stream != null) {
                stream.close();
            }
        }
        return str;
    }

    private InputStream downloadUrl(String urlString, String image) throws IOException {
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setReadTimeout(10000 /* milliseconds */);
        conn.setConnectTimeout(15000 /* milliseconds */);
        conn.setRequestMethod("POST");
        conn.setDoInput(true);
        conn.setDoOutput(true);
        conn.connect();


        Log.d("TAG", urlString);
        Log.d("TAG", image);

        Bitmap bmp = BitmapFactory.decodeFile(image);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 0, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream.toByteArray();
        image = Base64.encodeToString(byteArray, Base64.NO_WRAP);
        Log.d("TAG", Integer.toString(image.length()));
        conn.getOutputStream().write( ("image=" + image).getBytes());


        // Start the query
        Log.d("TAG", Integer.toString(conn.getResponseCode()));
        InputStream stream = conn.getInputStream();
        return stream;
    }

    /** Reads an InputStream and converts it to a String.
     * @param stream InputStream containing HTML from targeted site.
     * @param len Length of string that this method returns.
     * @return String concatenated according to len parameter.
     * @throws java.io.IOException
     * @throws java.io.UnsupportedEncodingException
     */
    private String readIt(InputStream stream, int len) throws IOException, UnsupportedEncodingException {
        Reader reader = null;
        reader = new InputStreamReader(stream, "UTF-8");
        char[] buffer = new char[len];
        reader.read(buffer);
        return new String(buffer);
    }
}
