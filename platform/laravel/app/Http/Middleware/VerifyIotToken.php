<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class VerifyIotToken
{
    public function handle(Request $request, Closure $next): Response
    {
        $expected = config('iot.api_token');
        $token = $request->header('X-API-Token')
            ?? $request->bearerToken()
            ?? $request->input('token');

        if (! is_string($token) || ! hash_equals((string) $expected, $token)) {
            return response()->json([
                'ok' => false,
                'message' => 'Unauthorized: token required / invalid',
            ], 401);
        }

        return $next($request);
    }
}
