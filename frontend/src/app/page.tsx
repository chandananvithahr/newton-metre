import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="flex items-center justify-between px-4 sm:px-8 py-5 border-b border-gray-100">
        <span className="text-xl font-bold tracking-tight text-primary-700 py-2">Costimize</span>
        <Link
          href="/login"
          className="bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-sm"
        >
          Try it free
        </Link>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-slate-50" />
        <div className="relative max-w-4xl mx-auto px-4 sm:px-8 py-16 sm:py-28 text-center">
          <div className="inline-block mb-6 px-4 py-1.5 bg-primary-100 text-primary-700 rounded-full text-sm font-medium animate-fade-in-up">
            Physics-based cost estimation
          </div>
          <h1 className="text-3xl sm:text-5xl md:text-6xl font-extrabold mb-6 leading-tight tracking-tight text-gray-900 animate-fade-in-up-delay-1">
            Know the real cost<br />
            <span className="text-primary-600">before you negotiate.</span>
          </h1>
          <p className="text-xl text-gray-500 mb-10 max-w-2xl mx-auto leading-relaxed animate-fade-in-up-delay-2">
            AI-powered should-cost breakdowns for mechanical parts.
            Line by line. Physics-based. Accurate to ±10%.
          </p>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/25 animate-fade-in-up-delay-3"
          >
            Get your first estimate free
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-5xl mx-auto px-4 sm:px-8 py-12 sm:py-20">
        <h2 className="text-3xl font-bold mb-4 text-center tracking-tight">How it works</h2>
        <p className="text-gray-500 text-center mb-12 max-w-xl mx-auto">
          Upload a drawing, get a detailed cost breakdown in under 60 seconds.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              num: "01",
              title: "Upload drawing",
              desc: "PDF or image of your engineering drawing — any format.",
              icon: (
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              ),
            },
            {
              num: "02",
              title: "AI analyzes",
              desc: "Extracts dimensions, tolerances, material, and manufacturing processes.",
              icon: (
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                </svg>
              ),
            },
            {
              num: "03",
              title: "Get breakdown",
              desc: "Line-by-line should-cost with material, machining, labour, and overhead.",
              icon: (
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
                </svg>
              ),
            },
          ].map((step) => (
            <div key={step.num} className="relative bg-white border border-gray-100 rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-sm font-bold text-primary-600 font-mono">{step.num}</span>
                <div className="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600">
                  {step.icon}
                </div>
              </div>
              <h3 className="font-semibold text-lg mb-2">{step.title}</h3>
              <p className="text-gray-500 leading-relaxed">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Industries */}
      <section className="bg-gradient-to-b from-slate-50 to-slate-100 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4 tracking-tight">Built for procurement teams</h2>
          <p className="text-gray-500 mb-6">
            Defense, aerospace, and automotive manufacturers across India.
          </p>
          <div className="flex flex-wrap justify-center gap-3 mb-10">
            {["Turned parts", "Milled parts", "Sheet metal"].map((tag) => (
              <span key={tag} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium text-gray-700">
                {tag}
              </span>
            ))}
          </div>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/25"
          >
            Get started free
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8 text-center text-sm text-gray-400">
        <p>&copy; 2026 Costimize. Should-cost intelligence for manufacturing.</p>
      </footer>
    </div>
  );
}
