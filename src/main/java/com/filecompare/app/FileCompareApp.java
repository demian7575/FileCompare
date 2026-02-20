package com.filecompare.app;

import com.filecompare.model.OperationRow;
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.ToolBar;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.stage.Stage;

public class FileCompareApp extends Application {

    private final ObservableList<OperationRow> rows = FXCollections.observableArrayList();

    @Override
    public void start(Stage stage) {
        stage.setTitle("FileCompare - Preview-first File Organizer");

        var root = new BorderPane();
        root.setPadding(new Insets(10));

        var statusLabel = new Label("Ready: 폴더를 선택하고 미리보기를 생성하세요.");
        var toolbar = createToolbar(statusLabel);
        root.setTop(toolbar);

        var table = createPreviewTable();
        root.setCenter(table);

        var footer = new HBox(statusLabel);
        footer.setPadding(new Insets(8, 0, 0, 0));
        root.setBottom(footer);

        var scene = new Scene(root, 1200, 700);
        stage.setScene(scene);
        stage.show();
    }

    private ToolBar createToolbar(Label statusLabel) {
        var selectFolderButton = new Button("폴더 선택");
        var generatePreviewButton = new Button("미리보기 생성");
        var applyButton = new Button("실행");

        selectFolderButton.setOnAction(event -> statusLabel.setText("샘플: D:/Downloads 폴더가 선택되었습니다."));
        generatePreviewButton.setOnAction(event -> {
            rows.setAll(sampleRows());
            statusLabel.setText("미리보기 생성 완료: " + rows.size() + "건");
        });
        applyButton.setOnAction(event -> statusLabel.setText("안전 모드: 현재는 미리보기만 제공됩니다."));

        var spacer = new HBox();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        return new ToolBar(selectFolderButton, generatePreviewButton, applyButton, spacer,
                new Label("기본 정책: Preview -> Confirm -> Apply"));
    }

    private TableView<OperationRow> createPreviewTable() {
        var table = new TableView<OperationRow>();

        var typeColumn = new TableColumn<OperationRow, String>("Type");
        typeColumn.setCellValueFactory(new PropertyValueFactory<>("type"));
        typeColumn.setPrefWidth(100);

        var sourceColumn = new TableColumn<OperationRow, String>("Source");
        sourceColumn.setCellValueFactory(new PropertyValueFactory<>("source"));
        sourceColumn.setPrefWidth(330);

        var targetColumn = new TableColumn<OperationRow, String>("Target");
        targetColumn.setCellValueFactory(new PropertyValueFactory<>("target"));
        targetColumn.setPrefWidth(330);

        var reasonColumn = new TableColumn<OperationRow, String>("Reason");
        reasonColumn.setCellValueFactory(new PropertyValueFactory<>("reason"));
        reasonColumn.setPrefWidth(250);

        var conflictColumn = new TableColumn<OperationRow, String>("Conflict");
        conflictColumn.setCellValueFactory(new PropertyValueFactory<>("conflictStatus"));
        conflictColumn.setPrefWidth(140);

        table.getColumns().addAll(typeColumn, sourceColumn, targetColumn, reasonColumn, conflictColumn);
        table.setItems(rows);
        table.setPlaceholder(new Label("미리보기 데이터가 없습니다."));

        return table;
    }

    private ObservableList<OperationRow> sampleRows() {
        return FXCollections.observableArrayList(
                new OperationRow(
                        "MOVE",
                        "D:/Downloads/receipt_2025_11.pdf",
                        "D:/Archive/Documents/receipt_2025_11.pdf",
                        "Rule: ext=pdf -> Documents",
                        "NONE"
                ),
                new OperationRow(
                        "RENAME",
                        "D:/Downloads/IMG_0001.JPG",
                        "D:/Downloads/2026-02-20_IMG_0001.JPG",
                        "Rule: camera files normalize",
                        "NONE"
                ),
                new OperationRow(
                        "DELETE",
                        "D:/Downloads/copy_movie.mkv",
                        "(Recycle Bin)",
                        "Duplicate hash match group #14",
                        "PROTECTED"
                )
        );
    }

    public static void main(String[] args) {
        launch(args);
    }
}
