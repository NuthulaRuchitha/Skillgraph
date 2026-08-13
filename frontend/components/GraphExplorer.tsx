"use client";

import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import type { GraphNode, SkillGraph } from "@/lib/api";

const ForceGraph2D = dynamic(
  () => import("react-force-graph-2d"),
  {
    ssr: false,
  }
);

interface GraphExplorerProps {
  graph: SkillGraph;
}

interface GraphLink {
  source: string;
  target: string;
  type: string;
}

interface ForceGraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

const NODE_COLORS: Record<string, string> = {
  Job: "#22c55e",
  Skill: "#3b82f6",
  Technology: "#06b6d4",
  Company: "#a855f7",
  Location: "#f59e0b",
  Industry: "#ec4899",
};

export default function GraphExplorer({
  graph,
}: GraphExplorerProps) {
  const [width, setWidth] = useState(900);

  useEffect(() => {
    function updateWidth() {
      setWidth(
        Math.max(
          600,
          Math.min(window.innerWidth - 48, 1200)
        )
      );
    }

    updateWidth();

    window.addEventListener("resize", updateWidth);

    return () => {
      window.removeEventListener("resize", updateWidth);
    };
  }, []);

  /*
   * Merge nodes with the same name for visualization.
   *
   * Example:
   *   Spring Boot [Skill]
   *   Spring Boot [Technology]
   *
   * becomes one visual node.
   *
   * The backend data is NOT changed.
   */
  const data = useMemo<ForceGraphData>(() => {
    const visualNodes = new Map<string, GraphNode>();
    const idMap = new Map<string, string>();

    for (const node of graph.nodes) {
      const key = node.name.trim().toLowerCase();

      const existing = visualNodes.get(key);

      if (existing) {
        idMap.set(node.id, existing.id);
      } else {
        visualNodes.set(key, node);
        idMap.set(node.id, node.id);
      }
    }

    const links: GraphLink[] = graph.relationships
      .map((relationship) => ({
        source:
          idMap.get(relationship.source) ??
          relationship.source,

        target:
          idMap.get(relationship.target) ??
          relationship.target,

        type: relationship.type,
      }))
      .filter(
        (link) => link.source !== link.target
      );

    return {
      nodes: Array.from(visualNodes.values()),
      links,
    };
  }, [graph]);

  if (!graph.nodes.length) {
    return (
      <div className="flex h-[500px] items-center justify-center rounded-2xl border border-white/10 bg-white/[0.03]">
        <p className="text-sm text-slate-500">
          No graph data found.
        </p>
      </div>
    );
  }

  return (
    <section className="w-full">
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">
          Skill Graph
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Explore relationships between jobs, skills,
          technologies, companies and industries.
        </p>
      </div>

      {/* Legend */}
      <div className="mb-4 flex flex-wrap gap-4 rounded-xl border border-white/10 bg-slate-950 px-4 py-3">
        {Object.entries(NODE_COLORS).map(
          ([label, color]) => (
            <div
              key={label}
              className="flex items-center gap-2"
            >
              <span
                className="h-3 w-3 rounded-full"
                style={{
                  backgroundColor: color,
                }}
              />

              <span className="text-xs text-slate-400">
                {label}
              </span>
            </div>
          )
        )}
      </div>

      {/* Graph */}
      <div className="overflow-hidden rounded-2xl border border-white/10 bg-slate-950">
        <ForceGraph2D
          graphData={data}
          width={width}
          height={600}
          backgroundColor="#020617"

          dagMode="radialout"
          dagLevelDistance={170}

          nodeLabel={(node) => {
            const graphNode = node as GraphNode;

            return `${graphNode.label}: ${graphNode.name}`;
          }}

          nodeRelSize={8}

          linkDirectionalArrowLength={5}
          linkDirectionalArrowRelPos={1}

          linkColor={() =>
            "rgba(148, 163, 184, 0.45)"
          }

          linkLabel={(link) => {
            const graphLink = link as GraphLink;

            return graphLink.type;
          }}

          cooldownTicks={120}
          d3AlphaDecay={0.02}
          d3VelocityDecay={0.3}

          nodeCanvasObject={(
            node,
            ctx,
            globalScale
          ) => {
            const graphNode =
              node as GraphNode;

            const x = node.x ?? 0;
            const y = node.y ?? 0;

            const radius =
              graphNode.label === "Job"
                ? 11
                : 8;

            const color =
              NODE_COLORS[
                graphNode.label
              ] ?? "#94a3b8";

            /*
             * Node
             */
            ctx.beginPath();

            ctx.arc(
              x,
              y,
              radius,
              0,
              2 * Math.PI
            );

            ctx.fillStyle = color;
            ctx.fill();

            /*
             * Small white border
             */
            ctx.strokeStyle =
              "rgba(255,255,255,0.7)";

            ctx.lineWidth = 1;

            ctx.stroke();

            /*
             * Label
             */
            const fontSize = Math.max(
              9,
              Math.min(
                14,
                13 / globalScale
              )
            );

            ctx.font = `600 ${fontSize}px Sans-Serif`;

            ctx.textAlign = "center";
            ctx.textBaseline = "top";

            ctx.fillStyle = "#e2e8f0";

            /*
             * Wrap long labels
             */
            const maxWidth = 130;

            const words =
              graphNode.name.split(" ");

            const lines: string[] = [];

            let currentLine = "";

            for (const word of words) {
              const testLine =
                currentLine
                  ? `${currentLine} ${word}`
                  : word;

              if (
                ctx.measureText(testLine)
                  .width > maxWidth &&
                currentLine
              ) {
                lines.push(currentLine);
                currentLine = word;
              } else {
                currentLine = testLine;
              }
            }

            if (currentLine) {
              lines.push(currentLine);
            }

            lines.forEach(
              (line, index) => {
                ctx.fillText(
                  line,
                  x,
                  y +
                    radius +
                    5 +
                    index *
                      (fontSize + 2)
                );
              }
            );
          }}
        />
      </div>

      {/* Relationship hint */}
      <p className="mt-3 text-xs text-slate-500">
        Drag nodes to explore the graph • Scroll to
        zoom • Hover nodes and connections for details
      </p>
    </section>
  );
}