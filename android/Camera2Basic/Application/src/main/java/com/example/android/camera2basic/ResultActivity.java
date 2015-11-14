package com.example.android.camera2basic;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.media.ExifInterface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.Toast;

import com.microsoft.projectoxford.face.FaceServiceClient;
import com.microsoft.projectoxford.face.*;

import com.microsoft.projectoxford.face.contract.*;


import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;

/**
 * Created by suhon_000 on 11/14/2015.
 */
public class ResultActivity extends Activity {

    private FaceServiceClient faceServiceClient =
            new FaceServiceClient("6c15189c7c5c4dc3bd57e7bc43b5c5d9");

    private ImageView img;
    private Bitmap origBmp;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);
        String path = getIntent().getStringExtra("TESTING");
        origBmp = BitmapFactory.decodeFile(path);
        origBmp = rotateImage(origBmp, 270);
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

        detectAndFrame(origBmp);
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


    private Bitmap rotateImage(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(), matrix, true);
    }


}