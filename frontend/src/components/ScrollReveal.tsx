"use client";

import { useEffect, useRef } from "react";

interface ScrollRevealProps {
  children: React.ReactNode;
  className?: string;
  /** Stagger delay in ms for child elements */
  stagger?: number;
  /** Reveal direction */
  direction?: "up" | "left" | "right" | "none";
  /** Use clip-path reveal instead of translate */
  clipReveal?: boolean;
}

export function ScrollReveal({
  children,
  className = "",
  stagger = 0,
  direction = "up",
  clipReveal = false,
}: ScrollRevealProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Check reduced motion preference
    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          if (prefersReduced) {
            el.style.opacity = "1";
          } else {
            el.classList.add("revealed");
          }
          obs.unobserve(el);
        }
      },
      { threshold: 0.15, rootMargin: "-60px" }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const baseStyle = clipReveal
    ? "clip-reveal"
    : direction === "left"
    ? "reveal-left"
    : direction === "right"
    ? "reveal-right"
    : direction === "none"
    ? "reveal-fade"
    : "reveal-up";

  return (
    <div
      ref={ref}
      className={`${baseStyle} ${className}`}
      style={stagger ? { transitionDelay: `${stagger}ms`, animationDelay: `${stagger}ms` } as React.CSSProperties : undefined}
    >
      {children}
    </div>
  );
}

/** Wraps each child with staggered reveal */
export function StaggerReveal({
  children,
  className = "",
  delayStep = 60,
  direction = "up",
}: {
  children: React.ReactNode;
  className?: string;
  delayStep?: number;
  direction?: "up" | "left" | "right" | "none";
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          const items = el.querySelectorAll("[data-stagger-item]");
          items.forEach((item, i) => {
            const htmlItem = item as HTMLElement;
            if (prefersReduced) {
              htmlItem.style.opacity = "1";
            } else {
              htmlItem.style.transitionDelay = `${i * delayStep}ms`;
              htmlItem.classList.add("revealed");
            }
          });
          obs.unobserve(el);
        }
      },
      { threshold: 0.1, rootMargin: "-40px" }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [delayStep]);

  const itemClass = direction === "left" ? "reveal-left" : direction === "none" ? "reveal-fade" : "reveal-up";

  return (
    <div ref={ref} className={className} data-stagger-container data-item-class={itemClass}>
      {children}
    </div>
  );
}

/** Mark a child as a stagger item */
export function StaggerItem({
  children,
  className = "",
  direction = "up",
}: {
  children: React.ReactNode;
  className?: string;
  direction?: "up" | "left" | "right" | "none";
}) {
  const baseClass = direction === "left" ? "reveal-left" : direction === "none" ? "reveal-fade" : "reveal-up";
  return (
    <div data-stagger-item className={`${baseClass} ${className}`}>
      {children}
    </div>
  );
}
