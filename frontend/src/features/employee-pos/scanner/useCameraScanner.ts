"use client"

import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react"
import {
  BrowserQRCodeReader,
  type IScannerControls,
} from "@zxing/browser"

type UseCameraScannerOptions = {
  onDetected: (identifier: string) => void
}

function getCameraErrorMessage(error: unknown) {
  if (error instanceof DOMException) {
    if (
      error.name === "NotAllowedError" ||
      error.name === "SecurityError"
    ) {
      return "Camera permission was denied. Allow camera access or use manual scan."
    }

    if (
      error.name === "NotFoundError" ||
      error.name === "DevicesNotFoundError"
    ) {
      return "No camera was found on this device."
    }

    if (
      error.name === "NotReadableError" ||
      error.name === "TrackStartError"
    ) {
      return "The camera is already in use by another application."
    }

    if (error.name === "OverconstrainedError") {
      return "The preferred camera is unavailable on this device."
    }
  }

  return "Unable to start the camera. Use manual scan instead."
}

export function useCameraScanner({
  onDetected,
}: UseCameraScannerOptions) {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const controlsRef = useRef<IScannerControls | null>(null)
  const hasDetectedRef = useRef(false)

  const [isCameraActive, setIsCameraActive] = useState(false)
  const [isStartingCamera, setIsStartingCamera] = useState(false)
  const [cameraError, setCameraError] = useState<string | null>(null)

  const stopCamera = useCallback(() => {
    controlsRef.current?.stop()
    controlsRef.current = null
    hasDetectedRef.current = false

    const videoElement = videoRef.current
    const stream = videoElement?.srcObject

    if (stream instanceof MediaStream) {
      stream.getTracks().forEach((track) => track.stop())
    }

    if (videoElement) {
      videoElement.srcObject = null
    }

    setIsCameraActive(false)
    setIsStartingCamera(false)
  }, [])

  const startCamera = useCallback(async () => {
    if (
      isCameraActive ||
      isStartingCamera ||
      !videoRef.current
    ) {
      return
    }

    try {
      setIsStartingCamera(true)
      setCameraError(null)
      hasDetectedRef.current = false

      const reader = new BrowserQRCodeReader()

      const controls = await reader.decodeFromConstraints(
        {
          audio: false,
          video: {
            facingMode: {
              ideal: "environment",
            },
          },
        },
        videoRef.current,
        (result) => {
          if (!result || hasDetectedRef.current) {
            return
          }

          const identifier = result.getText().trim()

          if (!identifier) {
            return
          }

          hasDetectedRef.current = true
          onDetected(identifier)
          stopCamera()
        }
      )

      controlsRef.current = controls
      setIsCameraActive(true)
    } catch (error) {
      stopCamera()
      setCameraError(getCameraErrorMessage(error))
    } finally {
      setIsStartingCamera(false)
    }
  }, [
    isCameraActive,
    isStartingCamera,
    onDetected,
    stopCamera,
  ])

  useEffect(() => {
    const videoElement = videoRef.current

    return () => {
      controlsRef.current?.stop()
      controlsRef.current = null

      const stream = videoElement?.srcObject

      if (stream instanceof MediaStream) {
        stream.getTracks().forEach((track) => track.stop())
      }

      if (videoElement) {
        videoElement.srcObject = null
      }
    }
  }, [])

  return {
    videoRef,
    isCameraActive,
    isStartingCamera,
    cameraError,
    startCamera,
    stopCamera,
  }
}