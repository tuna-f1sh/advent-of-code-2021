#[aoc_generator(day1)]
pub fn input_generator(input: &str) -> Vec<u64> {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.parse().unwrap())
        .collect()
}

#[aoc(day1, part1)]
pub fn part_01(input: &Vec<u64>) -> Result<u64, &str> {
    Ok(input
        .windows(2)
        .filter(|pair| pair[1] > pair[0])
        .count() as u64)
}

#[aoc(day1, part2)]
pub fn part_02(input: &Vec<u64>) -> Result<u64, &str> {
    Ok(input
        .windows(4)
        .filter(|quartet| quartet[3] > quartet[0])
        .count() as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263";

    #[test]
    fn part1_example() {
        assert_eq!(part_01(&input_generator(&EXAMPLE)).unwrap(), 7);
    }

    #[test]
    fn part2_example() {
        assert_eq!(part_02(&input_generator(&EXAMPLE)).unwrap(), 5);
    }
}
