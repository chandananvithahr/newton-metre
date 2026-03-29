import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      <nav className="flex items-center justify-between px-8 py-4 border-b">
        <span className="text-xl font-bold">Costimize</span>
        <Link href="/login" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          Try it free
        </Link>
      </nav>

      <section className="max-w-4xl mx-auto px-8 py-24 text-center">
        <h1 className="text-5xl font-bold mb-6">
          Know the real cost before you negotiate.
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          AI-powered should-cost breakdowns for mechanical parts.
          Line by line. Physics-based. Accurate to ±10%.
        </p>
        <Link href="/login" className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg hover:bg-blue-700 inline-block">
          Try it free
        </Link>
      </section>

      <section className="max-w-4xl mx-auto px-8 py-16">
        <h2 className="text-3xl font-bold mb-8 text-center">How it works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6">
            <div className="text-4xl mb-4">1</div>
            <h3 className="font-semibold mb-2">Upload drawing</h3>
            <p className="text-gray-600">PDF or image of your engineering drawing</p>
          </div>
          <div className="text-center p-6">
            <div className="text-4xl mb-4">2</div>
            <h3 className="font-semibold mb-2">AI analyzes</h3>
            <p className="text-gray-600">Extracts dimensions, tolerances, and processes</p>
          </div>
          <div className="text-center p-6">
            <div className="text-4xl mb-4">3</div>
            <h3 className="font-semibold mb-2">Get breakdown</h3>
            <p className="text-gray-600">Line-by-line should-cost in seconds</p>
          </div>
        </div>
      </section>

      <section className="bg-gray-100 py-16">
        <div className="max-w-4xl mx-auto px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Built for procurement teams</h2>
          <p className="text-gray-600 mb-8">Defense, aerospace, and automotive manufacturers</p>
          <Link href="/login" className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg hover:bg-blue-700 inline-block">
            Get started free
          </Link>
        </div>
      </section>
    </div>
  );
}
