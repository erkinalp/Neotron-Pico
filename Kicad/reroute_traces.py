import pcbnew
import os

def clear_traces():
    print("Clearing existing traces to prepare for rerouting...")
    
    pcb_file = "neotron-pico-btx.kicad_pcb"
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    backup_file = "neotron-pico-btx.kicad_pcb.traces_backup"
    if not os.path.exists(backup_file):
        os.system(f"cp {pcb_file} {backup_file}")
        print(f"Created backup: {backup_file}")
    
    board = pcbnew.LoadBoard(pcb_file)
    print(f"Loaded PCB file: {pcb_file}")
    
    board_bbox = board.GetBoardEdgesBoundingBox()
    board_width = board_bbox.GetWidth() / 1000000.0  # Convert to mm
    board_height = board_bbox.GetHeight() / 1000000.0
    print(f"Board dimensions: {board_width:.2f} mm x {board_height:.2f} mm")
    
    tracks = list(board.GetTracks())
    track_count = len(tracks)
    print(f"Found {track_count} tracks to remove")
    
    for track in tracks:
        board.Remove(track)
    
    remaining_tracks = list(board.GetTracks())
    print(f"Remaining tracks after removal: {len(remaining_tracks)}")
    
    pcbnew.SaveBoard(pcb_file, board)
    print(f"Saved modified PCB to {pcb_file}")
    
    print("\nNOTE: Trace rerouting requires KiCad GUI for proper implementation.")
    print("The PCB file has been prepared by removing existing traces.")
    print("Please use KiCad's interactive router to manually reroute traces.")
    
    return True

if __name__ == "__main__":
    clear_traces()
