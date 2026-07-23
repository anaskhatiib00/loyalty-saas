"use client"

import {
  Camera,
  CameraOff,
  Loader2,
  ScanLine,
} from "lucide-react"

import { useCameraScanner } from "./useCameraScanner"

type CameraScannerProps = {
  disabled?: boolean
  onDetected: (identifier: string) => void
}

export function CameraScanner({
  disabled = false,
  onDetected,
}: CameraScannerProps) {
  const {
    videoRef,
    isCameraActive,
    isStartingCamera,
    cameraError,
    startCamera,
    stopCamera,
  } = useCameraScanner({
    onDetected,
  })

  return (
    <div className="flex flex-col">
      <div className="relative min-h-72 overflow-hidden rounded-[2rem] border border-emerald-300/20 bg-black">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className={`absolute inset-0 size-full object-cover transition ${
            isCameraActive ? "opacity-100" : "opacity-0"
          }`}
        />

        {isCameraActive ? (
          <>
            <div className="pointer-events-none absolute inset-0 bg-black/10" />

            <div className="pointer-events-none absolute inset-8 rounded-[1.5rem] border border-emerald-300/50">
              <div className="absolute left-0 top-0 size-8 rounded-tl-xl border-l-4 border-t-4 border-emerald-300" />
              <div className="absolute right-0 top-0 size-8 rounded-tr-xl border-r-4 border-t-4 border-emerald-300" />
              <div className="absolute bottom-0 left-0 size-8 rounded-bl-xl border-b-4 border-l-4 border-emerald-300" />
              <div className="absolute bottom-0 right-0 size-8 rounded-br-xl border-b-4 border-r-4 border-emerald-300" />

              <div className="absolute left-4 right-4 top-1/2 h-px bg-emerald-300 shadow-[0_0_16px_rgba(110,231,183,0.9)]" />
            </div>

            <div className="absolute bottom-5 left-1/2 -translate-x-1/2 rounded-full border border-white/10 bg-black/60 px-4 py-2 text-sm text-white backdrop-blur">
              Point the camera at the loyalty QR code
            </div>
          </>
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center px-6 text-center">
            <div className="flex size-24 items-center justify-center rounded-3xl bg-emerald-300 text-[#07110f] shadow-2xl shadow-emerald-500/20">
              {isStartingCamera ? (
                <Loader2 className="size-11 animate-spin" />
              ) : (
                <Camera className="size-11" />
              )}
            </div>

            <p className="mt-6 text-xl font-semibold">
              {isStartingCamera
                ? "Starting camera"
                : "Scan loyalty card"}
            </p>

            <p className="mt-2 max-w-md text-sm leading-6 text-white/50">
              Use the device camera to scan the customer loyalty QR code.
            </p>
          </div>
        )}
      </div>

      {cameraError ? (
        <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-100">
          {cameraError}
        </div>
      ) : null}

      <div className="mt-4">
        {isCameraActive ? (
          <button
            type="button"
            onClick={stopCamera}
            className="inline-flex h-12 w-full items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/[0.05] font-semibold text-white transition hover:bg-white/10"
          >
            <CameraOff className="size-5" />
            Stop camera
          </button>
        ) : (
          <button
            type="button"
            onClick={() => void startCamera()}
            disabled={disabled || isStartingCamera}
            className="inline-flex h-12 w-full items-center justify-center gap-2 rounded-2xl bg-emerald-300 font-semibold text-[#07110f] transition hover:bg-emerald-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isStartingCamera ? (
              <>
                <Loader2 className="size-5 animate-spin" />
                Starting camera
              </>
            ) : (
              <>
                <ScanLine className="size-5" />
                Start camera scan
              </>
            )}
          </button>
        )}
      </div>
    </div>
  )
}