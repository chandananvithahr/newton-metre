import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { NextResponse, type NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);

  // Supabase sends error params when confirmation fails (expired, invalid, etc.)
  const error = requestUrl.searchParams.get("error");
  const errorDescription = requestUrl.searchParams.get("error_description");
  if (error) {
    const loginUrl = new URL("/login", requestUrl.origin);
    loginUrl.searchParams.set("error", errorDescription || error);
    return NextResponse.redirect(loginUrl);
  }

  const code = requestUrl.searchParams.get("code");
  // token_hash flow: Supabase may send token_hash + type instead of code
  const tokenHash = requestUrl.searchParams.get("token_hash");
  const type = requestUrl.searchParams.get("type");

  if (!code && !tokenHash) {
    // No auth params at all — send to login
    return NextResponse.redirect(new URL("/login", requestUrl.origin));
  }

  const cookieStore = await cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet: { name: string; value: string; options?: Record<string, unknown> }[]) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options),
          );
        },
      },
    },
  );

  if (code) {
    const { error: exchangeError } = await supabase.auth.exchangeCodeForSession(code);
    if (exchangeError) {
      // Most common cause: user opened confirmation link in a different browser
      // where the PKCE verifier cookie doesn't exist.
      const loginUrl = new URL("/login", requestUrl.origin);
      loginUrl.searchParams.set(
        "error",
        "Confirmation failed. If you opened the email link in a different browser or device, " +
        "please open it in the same browser where you signed up. Or click 'Sign up' again to get a new link."
      );
      return NextResponse.redirect(loginUrl);
    }
    return NextResponse.redirect(new URL("/dashboard", requestUrl.origin));
  }

  if (tokenHash && type) {
    const { error: verifyError } = await supabase.auth.verifyOtp({
      type: type as "signup" | "recovery" | "email",
      token_hash: tokenHash,
    });
    if (verifyError) {
      const loginUrl = new URL("/login", requestUrl.origin);
      loginUrl.searchParams.set("error", "Confirmation link expired or already used. Please request a new one.");
      return NextResponse.redirect(loginUrl);
    }
    return NextResponse.redirect(new URL("/dashboard", requestUrl.origin));
  }

  return NextResponse.redirect(new URL("/login", requestUrl.origin));
}
