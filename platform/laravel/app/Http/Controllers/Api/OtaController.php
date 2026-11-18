<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\File;
use Symfony\Component\HttpFoundation\BinaryFileResponse;

class OtaController extends Controller
{
    public function firmwareV2(): BinaryFileResponse
    {
        $dir = storage_path('app/ota');
        File::ensureDirectoryExists($dir);
        $path = $dir.'/firmware_v2.bin';

        if (! File::exists($path)) {
            File::put($path, 'DHT_RGB_IOT_FW_V2_PLACEHOLDER_VERSION_2_0_0');
        }

        return response()->download($path, 'firmware_v2.bin', [
            'Content-Type' => 'application/octet-stream',
        ]);
    }

    public function info(): \Illuminate\Http\JsonResponse
    {
        $path = storage_path('app/ota/firmware_v2.bin');

        return response()->json([
            'v1' => [
                'version' => '1.0.0',
                'interval_ms' => 5000,
                'led_rule' => 'LED terpisah: hijau <25 | kuning 25-30 | merah >30',
            ],
            'v2' => [
                'version' => '2.0.0',
                'interval_ms' => 3000,
                'led_rule' => 'LED terpisah: hijau <24 | kuning 24-28 | merah >28',
                'ota_url' => url('/api/ota/firmware_v2.bin'),
                'bin_exists' => File::exists($path),
                'bin_size' => File::exists($path) ? File::size($path) : 0,
            ],
        ]);
    }
}
