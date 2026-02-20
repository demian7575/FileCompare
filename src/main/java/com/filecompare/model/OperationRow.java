package com.filecompare.model;

public record OperationRow(
        String type,
        String source,
        String target,
        String reason,
        String conflictStatus
) {
}
