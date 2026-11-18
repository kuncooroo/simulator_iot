<?php

use App\Http\Controllers\Api\CommandController;
use App\Http\Controllers\Api\OtaController;
use App\Http\Controllers\Api\TelemetryController;
use App\Http\Middleware\VerifyIotToken;
use Illuminate\Support\Facades\Route;

Route::get('/health', function () {
    return response()->json([
        'status' => 'ok',
        'service' => 'Simple DHT RGB IoT Laravel API',
        'device_id' => config('iot.device_id'),
        'time' => now()->toIso8601String(),
    ]);
});

Route::get('/telemetry/latest', [TelemetryController::class, 'latest']);
Route::get('/telemetry/status', [TelemetryController::class, 'status']);
Route::get('/ota/info', [OtaController::class, 'info']);
Route::get('/ota/firmware_v2.bin', [OtaController::class, 'firmwareV2']);

Route::post('/telemetry', [TelemetryController::class, 'store'])
    ->middleware(VerifyIotToken::class);

Route::post('/command', [CommandController::class, 'store'])
    ->middleware(VerifyIotToken::class);
