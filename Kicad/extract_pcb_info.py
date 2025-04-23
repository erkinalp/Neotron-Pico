import pcbnew

def extract_pcb_info(pcb_file):
    try:
        board = pcbnew.LoadBoard(pcb_file)
        
        board_bbox = board.GetBoardEdgesBoundingBox()
        width_mm = board_bbox.GetWidth() / 1000000.0  # Convert from internal units to mm
        height_mm = board_bbox.GetHeight() / 1000000.0
        
        print(f"Board dimensions: {width_mm:.2f} mm x {height_mm:.2f} mm")
        
        mounting_holes = []
        for module in board.GetFootprints():
            if "MountingHole" in module.GetFPID().GetLibItemName() or module.GetReference().startswith('H'):
                pos = module.GetPosition()
                x_mm = pos.x / 1000000.0
                y_mm = pos.y / 1000000.0
                mounting_holes.append((x_mm, y_mm))
        
        print("\nMounting hole positions:")
        for i, pos in enumerate(mounting_holes):
            print(f"Hole {i+1}: ({pos[0]:.2f} mm, {pos[1]:.2f} mm)")
        
        category_a_count = 0
        category_b_count = 0
        category_c_count = 0
        uncategorized = 0
        
        for module in board.GetFootprints():
            ref = module.GetReference()
            if ref.startswith('U') or ref.startswith('LOGO'):
                category_a_count += 1
            elif ref.startswith('R') or ref.startswith('C') or ref.startswith('NT') or ref.startswith('Q') or ref.startswith('TP') or ref.startswith('FB') or ref.startswith('Y') or ref.startswith('D') or ref.startswith('SW') or ref.startswith('BT') or ref.startswith('F') or ref.startswith('L'):
                category_b_count += 1
            elif ref.startswith('J') or ref.startswith('H') or ref.startswith('JP'):
                category_c_count += 1
            else:
                uncategorized += 1
        
        print("\nComponent counts by category:")
        print(f"Category A (Non-mirrorable): {category_a_count}")
        print(f"Category B (Mirrorable): {category_b_count}")
        print(f"Category C (Position-critical): {category_c_count}")
        print(f"Uncategorized: {uncategorized}")
        print(f"Total components: {category_a_count + category_b_count + category_c_count + uncategorized}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_pcb_info("neotron-pico-btx.kicad_pcb")
