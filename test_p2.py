import json
from environment import Environment
from backtrack import backtrack
from forecast import forecast


def run_p2_demo():
    print("=" * 60)
    print("TideX P2 MVP Lagrangian Oil-Spill Drift Demonstration")
    print("=" * 60)

    # 1. Initialize Environmental Handler
    print("\n[Step 1] Initializing Environmental Data (ERA5 & CMEMS)...")
    env = Environment()

    # 2. Define Synthetic Observed Spill Polygon near 15.0 N, 72.0 E
    observation_time = "2026-08-02T12:00:00Z"
    synthetic_spill_polygon = {
        "type": "Polygon",
        "coordinates": [[
            [71.98, 14.98],
            [72.02, 14.98],
            [72.02, 15.02],
            [71.98, 15.02],
            [71.98, 14.98]
        ]]
    }

    print(f"\n[Step 2] Synthetic Spill Observed at Lat 15.0, Lon 72.0")
    print(f"Observation Time: {observation_time}")

    # 3. Run Backtrack Simulation (24-hour hindcast)
    print("\n[Step 3] Running Backtrack (Hindcast) 24 hours into the past...")
    backtrack_results = backtrack(
        spill_polygon=synthetic_spill_polygon,
        observation_time=observation_time,
        duration_hours=24,
        num_particles=500,
        env=env
    )

    probable_source = backtrack_results["probable_source_region"]
    back_trajectories = backtrack_results["backward_trajectories"]
    back_uncertainty = backtrack_results["uncertainty_polygon"]

    print("\n--- BACKTRACK RESULTS SUMMARY ---")
    print(f"Probable Source Region Geometry Type: {probable_source['geometry']['type']}")
    print(f"Estimated Origin Time             : {probable_source['properties']['estimated_origin_time']}")
    print(f"Backward Trajectories Count       : {len(back_trajectories['features'])} particle paths")
    print(f"Uncertainty Polygon Geometry Type : {back_uncertainty['geometry']['type']}")

    # 4. Run Forecast Simulation (24-hour forecast from estimated origin)
    origin_start_time = probable_source['properties']['estimated_origin_time']
    print(f"\n[Step 4] Running Forecast 24 hours into the future starting from estimated origin ({origin_start_time})...")
    forecast_results = forecast(
        source_region=probable_source,
        start_time=origin_start_time,
        duration_hours=24,
        num_particles=500,
        env=env
    )

    fwd_trajectories = forecast_results["future_trajectories"]
    fwd_uncertainty = forecast_results["forecast_uncertainty_polygon"]

    print("\n--- FORECAST RESULTS SUMMARY ---")
    print(f"Forward Trajectories Count        : {len(fwd_trajectories['features'])} particle paths")
    print(f"Forecast Uncertainty Geometry Type: {fwd_uncertainty['geometry']['type']}")
    print(f"Forecast End Time                 : {fwd_uncertainty['properties']['forecast_end_time']}")

    # 5. Print GeoJSON Samples
    print("\n" + "=" * 60)
    print("GEOJSON OUTPUT DEMONSTRATION SAMPLES")
    print("=" * 60)

    print("\n1. Probable Source Region GeoJSON:")
    print(json.dumps(probable_source, indent=2))

    print("\n2. Sample Backward Trajectory Feature (Particle 0):")
    print(json.dumps(back_trajectories['features'][0], indent=2))

    print("\n3. Forecast Uncertainty Envelope GeoJSON:")
    print(json.dumps(fwd_uncertainty, indent=2))

    print("\n4. Sample Forward Trajectory Feature (Particle 0):")
    print(json.dumps(fwd_trajectories['features'][0], indent=2))

    print("\n" + "=" * 60)
    print("SUCCESS: TideX P2 MVP Lagrangian simulation completed cleanly!")
    print("=" * 60)


if __name__ == '__main__':
    run_p2_demo()
