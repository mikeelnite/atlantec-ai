import { useEffect, useState } from 'react';
import { ChevronLeft, ChevronRight, Github, Landmark, MapPin, Users, Wind } from 'lucide-react';
import ChatInterface from './components/ChatInterface';

const features = [
  {
    icon: MapPin,
    title: 'Gaeltacht Regions',
    desc: 'Discover Irish-speaking towns across all Gaeltacht counties in Ireland.',
  },
  {
    icon: Landmark,
    title: 'Heritage Sites',
    desc: 'Explore local heritage, ancient monuments, and cultural landmarks nearby.',
  },
  {
    icon: Wind,
    title: 'Irish Language',
    desc: 'Learn place names, words, and phrases from the living Irish language.',
  },
  {
    icon: Users,
    title: 'Volunteering',
    desc: 'Find meaningful ways to contribute to Gaeltacht communities.',
  },
];

const countySlides = [
  {
    county: 'Galway',
    subtitle: 'Connemara National Park and west Galway Gaeltacht country',
    image:
      'https://commons.wikimedia.org/wiki/Special:Redirect/file/Connemara%20National%20Park%20Galway.jpg',
  },
  {
    county: 'Donegal',
    subtitle: 'Slieve League cliffs and north-west Gaeltacht heritage',
    image:
      'https://commons.wikimedia.org/wiki/Special:Redirect/file/Slieve%20League%2C%20Co.%20Donegal.jpg',
  },
  {
    county: 'Kerry',
    subtitle: 'Dingle Peninsula, Corca Dhuibhne, and Atlantic coastal views',
    image:
      'https://commons.wikimedia.org/wiki/Special:Redirect/file/Dingle%20Peninsula.jpg',
  },
  {
    county: 'Mayo',
    subtitle: 'Achill landscapes, Atlantic weather, and island culture',
    image:
      'https://commons.wikimedia.org/wiki/Special:Redirect/file/Lough%20Doo%2C%20Achill%20Island%2C%20Co.%20Mayo.jpg',
  },
];

function CountySlider() {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % countySlides.length);
    }, 4500);

    return () => window.clearInterval(timer);
  }, []);

  const activeSlide = countySlides[activeIndex];

  return (
    <div className="relative overflow-hidden rounded-2xl border border-stone-100 shadow-sm min-h-[280px]">
      <img
        src={activeSlide.image}
        alt={activeSlide.county}
        className="absolute inset-0 h-full w-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-emerald-950 via-emerald-900/60 to-emerald-900/20" />

      <div className="relative flex min-h-[280px] flex-col justify-between p-5 text-white">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-200/90">
              County Spotlight
            </p>
            <h3 className="mt-2 text-2xl font-semibold">{activeSlide.county}</h3>
            <p className="mt-2 max-w-[18rem] text-sm leading-relaxed text-white/80">
              {activeSlide.subtitle}
            </p>
          </div>

          <div className="rounded-full border border-white/20 bg-white/10 px-3 py-1 text-xs text-white/85 backdrop-blur-sm">
            {activeIndex + 1} / {countySlides.length}
          </div>
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="flex gap-2">
            {countySlides.map((slide, index) => (
              <button
                key={slide.county}
                type="button"
                onClick={() => setActiveIndex(index)}
                className={`h-2.5 rounded-full transition-all ${
                  index === activeIndex ? 'w-8 bg-white' : 'w-2.5 bg-white/45 hover:bg-white/70'
                }`}
                aria-label={`Show ${slide.county}`}
              />
            ))}
          </div>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={() =>
                setActiveIndex((current) => (current - 1 + countySlides.length) % countySlides.length)
              }
              className="rounded-full border border-white/20 bg-white/10 p-2 text-white backdrop-blur-sm transition-colors hover:bg-white/20"
              aria-label="Previous county"
            >
              <ChevronLeft size={16} />
            </button>
            <button
              type="button"
              onClick={() => setActiveIndex((current) => (current + 1) % countySlides.length)}
              className="rounded-full border border-white/20 bg-white/10 p-2 text-white backdrop-blur-sm transition-colors hover:bg-white/20"
              aria-label="Next county"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-stone-50 font-sans">
      <header className="relative overflow-hidden bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-900">
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              'url("https://images.pexels.com/photos/2832034/pexels-photo-2832034.jpeg?auto=compress&cs=tinysrgb&w=1920")',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-emerald-900/60 via-emerald-900/40 to-emerald-900/80" />

        <nav className="relative z-10 flex items-center justify-between px-6 py-4 max-w-6xl mx-auto">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-white/10 backdrop-blur border border-white/20 flex items-center justify-center">
              <Wind size={16} className="text-emerald-300" />
            </div>
            <span className="text-white font-semibold text-sm tracking-wide">Atlantec AI</span>
          </div>
          <a
            href="https://github.com/mikeelnite/atlantec-ai"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-white/70 hover:text-white text-xs transition-colors"
          >
            <Github size={14} />
            <span>GitHub</span>
          </a>
        </nav>

        <div className="relative z-10 px-6 pt-12 pb-20 max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur border border-white/20 rounded-full px-3 py-1 mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-white/80 text-xs font-medium">Atlantec AI Challenge 2026</span>
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4 leading-tight">
            Help Your
            <span className="block text-emerald-300">Gaeltacht</span>
          </h1>

          <p className="text-white/70 text-base md:text-lg max-w-xl mx-auto leading-relaxed">
            An AI-powered guide to Ireland&apos;s Irish-speaking regions. Discover towns,
            heritage sites, pubs, and ways to connect with living Irish culture.
          </p>

          <div className="flex items-center justify-center gap-6 mt-8 text-white/50 text-xs">
            <span className="flex items-center gap-1.5">
              <span className="w-1 h-1 rounded-full bg-emerald-400" />
              Tailte Eireann Data
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-1 h-1 rounded-full bg-teal-400" />
              OpenStreetMap
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 md:px-6 -mt-10 pb-16 relative z-10">
        <div className="grid lg:grid-cols-5 gap-6 items-start">
          <div className="lg:col-span-3">
            <div
              className="bg-white rounded-2xl shadow-xl border border-stone-100 overflow-hidden flex flex-col"
              style={{ height: '620px' }}
            >
              <ChatInterface />
            </div>
          </div>

          <aside className="lg:col-span-2 space-y-4">
            <div className="bg-white rounded-2xl border border-stone-100 shadow-sm overflow-hidden">
              <div className="px-4 py-3 border-b border-stone-50">
                <h3 className="text-xs font-semibold text-stone-500 uppercase tracking-wider">
                  What you can explore
                </h3>
              </div>
              <div className="divide-y divide-stone-50">
                {features.map(({ icon: Icon, title, desc }) => (
                  <div
                    key={title}
                    className="flex gap-3 px-4 py-3.5 hover:bg-stone-50/50 transition-colors"
                  >
                    <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Icon size={14} className="text-emerald-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-stone-700">{title}</p>
                      <p className="text-xs text-stone-400 mt-0.5 leading-relaxed">{desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <CountySlider />

            <div className="bg-emerald-50 rounded-2xl border border-emerald-100 p-4">
              <p className="text-xs font-semibold text-emerald-800 mb-1">About this project</p>
              <p className="text-xs text-emerald-700/80 leading-relaxed">
                Built by Team State Machines for the Atlantec AI Challenge 2026, using
                open government datasets from Ireland&apos;s data portal and the Gemini API to
                help communities discover and engage with Gaeltacht culture.
              </p>
            </div>
          </aside>
        </div>
      </main>

      <footer className="border-t border-stone-100 bg-white">
        <div className="max-w-6xl mx-auto px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-2">
          <p className="text-xs text-stone-400">
            Data sourced from Tailte Eireann &amp; OpenStreetMap under Creative Commons
          </p>
          <p className="text-xs text-stone-400">
            Atlantec AI Challenge 2026 &middot; Team State Machines
          </p>
        </div>
      </footer>
    </div>
  );
}
