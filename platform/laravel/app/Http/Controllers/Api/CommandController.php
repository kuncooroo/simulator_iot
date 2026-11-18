<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CommandController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'action' => ['required', 'string', 'max:64'],
            'note' => ['nullable', 'string', 'max:255'],
            'token' => ['nullable', 'string'],
        ]);

        return response()->json([
            'ok' => true,
            'message' => "command '{$data['action']}' accepted",
            'action' => $data['action'],
            'note' => $data['note'] ?? null,
            'hint' => $data['action'] === 'ota_update'
                ? 'Kirim action ota_update ke topic MQTT command agar ESP32 unduh firmware v2.'
                : null,
        ]);
    }
}
