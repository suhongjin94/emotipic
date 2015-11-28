//
//  ViewController.swift
//  emotipic
//
//  Created by GC on 11/26/15.
//  Copyright © 2015 emotipic. All rights reserved.
//

import UIKit
import AVFoundation
import CoreGraphics
import Alamofire

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    

    @IBOutlet weak var cameraView: UIView!
    @IBOutlet weak var tempImageView: UIImageView!
    @IBOutlet weak var takePhotoButton: UIButton!
    @IBOutlet weak var sendButton: UIButton!
    
    var captureSession : AVCaptureSession?
    var stillImageOutput : AVCaptureStillImageOutput?
    var previewLayer : AVCaptureVideoPreviewLayer?
    var didTakePhoto = Bool()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        previewLayer?.frame = cameraView.bounds
        self.tempImageView.contentMode = .ScaleAspectFit
    }
    
    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        
        captureSession = AVCaptureSession()
        captureSession?.sessionPreset = AVCaptureSessionPresetHigh
        
        do {
            var input : AVCaptureDeviceInput?
            
            let videoDevices = AVCaptureDevice.devicesWithMediaType(AVMediaTypeVideo)
            var captureDevice:AVCaptureDevice?
            
            for device in videoDevices {
                let device = device as! AVCaptureDevice
                if device.position == AVCaptureDevicePosition.Front {
                    captureDevice = device
                }
            }
            
            try input = AVCaptureDeviceInput(device : captureDevice)
            
            if captureSession?.canAddInput(input) != nil {
                captureSession?.addInput(input)
                
                stillImageOutput = AVCaptureStillImageOutput()
                stillImageOutput?.outputSettings = [AVVideoCodecKey : AVVideoCodecJPEG]
                
                if captureSession?.canAddOutput(stillImageOutput) != nil {
                    captureSession?.addOutput(stillImageOutput)
                    previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
                    previewLayer?.videoGravity = AVLayerVideoGravityResizeAspect
                    previewLayer?.connection.videoOrientation = AVCaptureVideoOrientation.Portrait
                    
                    cameraView.layer.addSublayer(previewLayer!)
                    captureSession?.startRunning()
                    print(previewLayer)
                    print(cameraView)
                }
            }
            
        } catch {
            print("input device is not working")
        }
    }
    

    func takePhoto() {
        if let videoConnection = stillImageOutput?.connectionWithMediaType(AVMediaTypeVideo) {
            videoConnection.videoOrientation = AVCaptureVideoOrientation.Portrait
            stillImageOutput?.captureStillImageAsynchronouslyFromConnection(videoConnection, completionHandler: {
                (sampleBuffer, error) in
                
                if sampleBuffer != nil {
                    let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(sampleBuffer)
                    let dataProvider = CGDataProviderCreateWithCFData(imageData)
                    let cgImageRef = CGImageCreateWithJPEGDataProvider(dataProvider, nil, true, CGColorRenderingIntent.RenderingIntentDefault)
                    
                    let image = UIImage(CGImage: cgImageRef!, scale: 1.0, orientation: UIImageOrientation.LeftMirrored)
                    
                    self.tempImageView.image = image
                    self.tempImageView.hidden = false
                    
                    
//                    Alamofire.request(.POST, "http://54.187.141.133:3000/")
//                        .responseJSON { response in
//                            if let JSON = response.result.value {
//                                print(JSON["response"])
//                                print("JSON: \(JSON)")
//                            }
//                    }
                }
            })
        }
    }
    
    @IBAction func takePhotoAction() {
        if didTakePhoto == true {
            tempImageView.hidden = true
            didTakePhoto = false
            self.sendButton.hidden = false
            takePhotoButton.setTitle("Take a Photo!", forState: UIControlState.Normal)
        }
        else{
            captureSession?.startRunning()
            didTakePhoto = true
            takePhoto()
            self.sendButton.hidden = false
            takePhotoButton.setTitle("Retake?", forState: UIControlState.Normal)
        }
    }
}

