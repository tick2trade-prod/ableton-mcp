"""Browser Agent for sample and preset browser integration.

Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)
Reference: Ableton Manual Section 5.4 "Hot-Swap Mode" (page 123)
"""

from .base_agent import AgentResult, BaseAgent


class BrowserAgent(BaseAgent):
    """Agent for sample and preset browser integration.

    Specializes in:
    - Sample search using Sound Similarity
    - Preset loading and browsing
    - Tag-based filtering
    """

    def __init__(self, **kwargs):
        super().__init__(name="BrowserAgent", **kwargs)

    def get_role(self) -> str:
        return "Browser and Library Manager"

    def get_goal(self) -> str:
        return "Efficiently search and load samples and presets"

    def search_samples(
        self,
        query: str,
        category: str | None = None,
        tags: list[str] | None = None,
        max_results: int = 10,
    ) -> AgentResult:
        """Search for samples in the browser.

        Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)

        Args:
            query: Search query (e.g., "909 kick")
            category: Category filter (e.g., "Drums", "Synths")
            tags: List of tags to filter by
            max_results: Maximum number of results

        Returns:
            AgentResult with search results
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Search samples '{query}'")
            return AgentResult(
                success=True,
                message=f"Mock: Found samples for '{query}'",
                data={
                    "query": query,
                    "category": category,
                    "tags": tags,
                    "results": ["sample1.wav", "sample2.wav"],
                },
            )

        try:
            # Search browser
            search_result = mcp.search_browser(
                query=query,
                category=category,
                tags=tags,
                max_results=max_results,
            )
            if not search_result.success:
                return AgentResult(
                    success=False,
                    message=f"Search failed: {search_result.message}",
                )

            results = search_result.data.get("results", [])
            self.log(f"Found {len(results)} samples for '{query}'")
            return AgentResult(
                success=True,
                message=f"Found {len(results)} samples",
                data={
                    "query": query,
                    "category": category,
                    "tags": tags,
                    "results": results,
                },
            )

        except Exception as e:
            self.log(f"Error searching samples: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    def load_similar_preset(
        self,
        track_name: str,
        reference_preset: str,
        device: str,
        similarity_threshold: float = 0.7,
    ) -> AgentResult:
        """Load preset using Sound Similarity.

        Reference: Ableton Manual Section 5.3 "Searching and Filtering" (page 120)

        Args:
            track_name: Target track name
            reference_preset: Reference preset name
            device: Device name (e.g., "Operator", "Wavetable")
            similarity_threshold: Similarity threshold (0.0-1.0)

        Returns:
            AgentResult with loaded preset details
        """
        mcp = self.get_mcp_client()
        if not mcp:
            self.log(f"Mock: Load similar preset for {track_name}")
            return AgentResult(
                success=True,
                message="Mock: Loaded similar preset",
                data={
                    "track_name": track_name,
                    "reference_preset": reference_preset,
                    "device": device,
                },
            )

        try:
            # Search for similar presets
            search_result = mcp.search_similar_presets(
                device=device,
                reference=reference_preset,
                threshold=similarity_threshold,
            )
            if not search_result.success or not search_result.data.get("results"):
                return AgentResult(
                    success=False,
                    message="No similar presets found",
                )

            # Load first result
            best_match = search_result.data["results"][0]
            load_result = mcp.load_preset(
                track_name=track_name,
                device_index=0,
                preset_name=best_match["name"],
            )
            if not load_result.success:
                return AgentResult(
                    success=False,
                    message=f"Failed to load preset: {load_result.message}",
                )

            self.log(f"Loaded similar preset '{best_match['name']}' to {track_name}")
            return AgentResult(
                success=True,
                message="Loaded similar preset",
                data={
                    "track_name": track_name,
                    "reference_preset": reference_preset,
                    "loaded_preset": best_match["name"],
                    "similarity": best_match.get("similarity", 1.0),
                },
            )

        except Exception as e:
            self.log(f"Error loading similar preset: {e}")
            return AgentResult(success=False, message=f"Error: {e}")

    async def execute(self, **kwargs) -> AgentResult:
        """Execute browser search and load tasks.

        Args:
            searches: List of {query, category, tags} dicts
            presets: List of {track, reference, device} dicts

        Returns:
            AgentResult with all search/load results
        """
        searches = kwargs.get("searches", [])
        presets = kwargs.get("presets", [])
        results = []
        errors = []

        # Execute searches
        for search in searches:
            result = self.search_samples(**search)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        # Load similar presets
        for preset in presets:
            result = self.load_similar_preset(**preset)
            if result.success:
                results.append(result.data)
            else:
                errors.extend(result.errors)

        return AgentResult(
            success=len(errors) == 0,
            message=f"Completed {len(results)} browser operations",
            data={"results": results},
            errors=errors,
        )
